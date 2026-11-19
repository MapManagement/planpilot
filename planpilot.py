#! /usr/bin/env python3
import logging
import os
import re
import sys
from subprocess import PIPE, Popen

from fasb import start_fasb, start_fasb_interpreter

import utils

TOKEN = re.compile(r'\(([A-Za-z0-9_\-]+)((?:\s+[A-Za-z0-9_\-]+)*)\)')

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s ::: %(message)s",
)
logger = logging.getLogger(__name__)

dirname = os.path.dirname(__file__)


def fix_path(path):
    return os.path.join(dirname, path)


def run_fd_translator(domain, instance):
    binary_path = fix_path("translate/translate.py")
    python_exec = sys.executable  # Uses the currently running Python interpreter
    command = [
        python_exec,
        binary_path,
        "--keep-unimportant-variables",
        domain,
        instance,
    ]
    time = utils.get_elapsed_time()
    process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
    stdout, stderr = process.communicate()
    # if stdout:
    #     print(stdout, file=sys.stdout, end='')

    if stderr:
        print(stderr, file=sys.stderr, end="")
    _, error = process.communicate()
    logging.info(f"translator time: {utils.get_elapsed_time() - time:.2f}s")

    logger.info(f"translator return code: {process.returncode}")
    if process.returncode != 0:
        print(error)
        exit(process.returncode)


def run_plasp(domain, instance, lp, encoding, dump_output, pddl_instance=True, hypotheses=None):
    binary_path = fix_path("bin/plasp")
    command = [binary_path, "translate", instance]  # SAS+ instance
    if pddl_instance:
        command = [binary_path, "translate", domain, instance]

    with open(lp, "w") as lp_file:
        # First, we add the corresponding sequential encoding to it
        encoding = fix_path("encodings/exact-sequential-horizon.lp")
        if args.encoding == "bounded":
            encoding = fix_path("encodings/bounded-sequential-horizon.lp")
        elif args.encoding == "recognition":
            encoding = fix_path("encodings/recognition-bounded-sequential-horizon.lp")

        with open(encoding) as seq_encoding:
            lp_file.write(seq_encoding.read())

        time_steps_encoding = fix_path("encodings/action-per-time-step.lp")
        if args.abstract_time_steps:
            time_steps_encoding = fix_path("encodings/abstract-time-steps.lp")

        with open(time_steps_encoding) as time_encoding:
            lp_file.write(time_encoding.read())

        if args.partial_plan:
            logger.info(f"Using partial plan '{args.partial_plan}'...")
            constraints: str | None = translate_partial_plan_into_constraints(
                args.partial_plan
            )
            lp_file.write("\n%%%%%%% partial plan encoding\n" + constraints + "\n")

        if args.add_constraints_file:
            logger.info(
                f"Using additional constraints of file '{args.add_constraints_file}'..."
            )
            try:
                with open(args.add_constraints_file, "r") as f:
                    constraints = f.readlines()
                    constraints = "".join(constraints)
                    lp_file.write(
                        "\n%%%%%%% partial plan encoding\n" + constraints + "\n"
                    )
            except IOError:
                print(
                    f"Error: File {args.add_constraints_file} does not appear to exist."
                )
                exit(1)

        if args.add_constraints:
            constraints = args.add_constraints.encode().decode("unicode_escape")
            lp_file.write("\n%%%%%%% partial plan encoding\n" + constraints + "\n")

        if args.encoding == "recognition":
            lp_file.write(generate_goal_hypotheses(hypotheses))
            lp_file.write("#show test_goal/1.")

        # Now, we run plasp to produce the instance-specific info
        process = Popen(command, stdout=lp_file, stdin=PIPE, stderr=PIPE, text=True)

    time = utils.get_elapsed_time()
    _, error = process.communicate()
    logging.info(f"plasp time: {utils.get_elapsed_time() - time:.2f}s")

    logger.info(f"plasp return code: {process.returncode}")
    if process.returncode != 0:
        print(error)
        exit(process.returncode)


def run_fasb(lp, horizon, script=None, is_recognition=False):
    # Parameter arguments are still needed for clingo
    clingo_args = ["-c", f"horizon={horizon}", "0"]

    if is_recognition:
        clingo_args.append("--project")

    # TODO: The parameter is reversed due to the Python bindings
    compute_facets = not args.dry

    if args.dry:
        logging.info("Dry startup...")
        logging.info(
            "To compute facets matching some regular expression 're', use the command '!? re'..."
        )

    time = utils.get_elapsed_time()
    try:
        if script:
            logger.info(f"Executing fasb script {script}...")
            start_fasb_interpreter(
                clingo_args,
                lp,
                fix_path(script),
                compute_facets,
                False,
            )
        else:
            logging.info(
                "Starting fasb... To quit the interactive mode, use the command ':q'."
            )
            start_fasb(clingo_args, lp, compute_facets, False)
    except Exception as exc:
        logger.error(f"fasb failed: {exc}")
        sys.exit(1)

    logging.info(f"fasb time: {utils.get_elapsed_time() - time:.2f}s")


def remove_lp_files():
    current_directory = os.getcwd()

    for file_name in os.listdir(current_directory):
        file_path = os.path.join(current_directory, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".lp"):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"Error removing {file_path}: {e}")


def translate_partial_plan_into_constraints(file_path: str) -> str | None:
    # TODO: give the name of specific format
    """
    Expects actions in specific format.

    Example:
    `a b c (1) d e (1)`
    will be translated into
    `
    :- not occurs(action(("a","b","c")),1).
    :- not occurs(action(("d","e")),2).
    `
    """
    global PARTIAL_PLAN_DELIMITER
    PARTIAL_PLAN_DELIMITER = "(1)"

    try:
        with open(file_path, "r") as f:
            actions = filter(
                lambda x: x,
                map(lambda x: x.strip(), f.read().split(PARTIAL_PLAN_DELIMITER)),
            )
            return "\n".join(
                map(
                    lambda t: translate_action_to_constraint(*t[::-1]),
                    enumerate(actions),
                )
            )
    except Exception as e:
        logger.error(f"could not read partial plan '{file_path}': {e}")


def translate_action_to_constraint(action: str, at: int) -> str:
    """
    Translates whitespace-separated action into integrity constraint.

    Example:
    `a b c` as first action will be translated into
    `:- not occurs(action(("a","b","c")),1).`
    """
    return (
        ":- not occurs(action(("
        + ",".join(map(lambda x: f'"{x}"', action.split(" ")))
        + f")),{at+1})."
    )

def goal_rec_set_pddl_goal(instance_file_path: str, hypotheses_file_path: str):
    with open(instance_file_path, "r") as instance_file:
        instance_content = instance_file.read()

    with open(hypotheses_file_path, "r") as hypotheses_file:
        first_hypothesis = hypotheses_file.readline()

    instance_h0_content = instance_content.replace("<HYPOTHESIS>", first_hypothesis)
    instance_h0_path = fix_path("benchmarks/goal_recognition/instance_h0.pddl")

    with open(instance_h0_path, "w+") as instance_h0_file:
        instance_h0_file.write(instance_h0_content)

    return instance_h0_path

def atom_name(pred, args):
    pred = pred.lower()
    args = [a.lower() for a in args]

    if args:
        return f"{pred}({', '.join(args)})"
    else:
        return pred

def generate_goal_hypotheses(hypotheses_file_path: str):
    lp_goal_hypotheses = ""

    with open(hypotheses_file_path, "r") as hypotheses_file:
        for hyp_number, line in enumerate(hypotheses_file.readlines()):
            line = line.strip()

            if not line:
                continue

            hyp_name = f"h{hyp_number}"
            lp_goal_hypotheses += f"\n%%%%% {hyp_name} %%%%%"
            lp_goal_hypotheses += f"\ncandidate_goal({hyp_name})."

            for pred, args in TOKEN.findall(line):
                if pred.upper() == "AND":
                    continue

                name = atom_name(pred, args.split())
                lp_goal_hypotheses += f'\nhyp_goal({hyp_name}, "{name}").'

            lp_goal_hypotheses += "\n"

    return lp_goal_hypotheses

def remove_fixed_goal_from_lp(lp_file_path: str):
    with open(lp_file_path, "r") as f:
        lines = [line for line in f if not line.startswith("goal(")]

    with open(lp_file_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    args = utils.parse_arguments()

    domain_file = args.domain
    instance_file = args.instance
    hypotheses_file = args.hypotheses

    if args.is_pddl_instance and not os.path.isfile(domain_file):
        sys.stderr.write("Error: Domain file does not exist.\n")
        sys.exit()
    if not os.path.isfile(instance_file):
        sys.stderr.write("Error: Instance file does not exist.\n")
        sys.exit()

    if args.encoding == "recognition" and not os.path.isfile(hypotheses_file):
        sys.stderr.write("Error: Mode recognition but hypotheses file does not exist.\n")
        sys.exit()

    if args.is_pddl_instance:
        logger.info("Running translator...")
        instance = args.instance

        if args.encoding == "recognition":
            instance = goal_rec_set_pddl_goal(args.instance, args.hypotheses)

        run_fd_translator(args.domain, instance)
        args.instance = "output.sas"
        # run_plasp(
        #     args.domain,
        #     args.instance,
        #     args.lp_name,
        #     args.encoding,
        #     args.dump_output)

    logger.info("Running plasp...")
    run_plasp("", args.instance, args.lp_name, args.encoding, args.dump_output, False, hypotheses_file)

    if args.encoding == "recognition":
        remove_fixed_goal_from_lp(args.lp_name)

    logger.info("Running fasb...")
    run_fasb(args.lp_name, args.horizon, args.script, args.encoding == "recognition")

    if args.cleanup:
        remove_lp_files()

    logging.info(f"Total time: {utils.get_elapsed_time():.2f}s")
    logger.info("Done!")
