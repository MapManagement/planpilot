pub const PROMPT: &str = "\x1b[35m::\x1b[0m ";
pub const ACTIVATE_FACETS: &str = "activate";
pub const ACTIVATE_FACETS_LT: &str = "activate!";
pub const ACTIVATE_FACETS_LAZY: &str = "lazy+";
pub const SHOW_FACETS: &str = "facets";
pub const COMPUTE_FACETS_SU: &str = "compute^";
pub const COMPUTE_FACETS: &str = "compute";
pub const FACET_COUNT: &str = "count";
pub const FACET_COUNTS: &str = "counts";
pub const FACET_COUNTS_PROJECTING: &str = "counts!";
pub const WEIGHTED_FACET_COUNT: &str = "wcount";
pub const WEIGHTED_FACET_COUNTS: &str = "wcounts";
pub const ANSWER_SET_COUNT: &str = "solvecount";
pub const ANSWER_SET_COUNTS: &str = "solvecounts";
pub const ENUMERATE_SOLUTIONS: &str = "solve";
pub const ENUMERATE_PROJECTED_SOLUTIONS: &str = "solve*";
pub const SHOW_ROUTE: &str = "route";
pub const CLEAR_ROUTE: &str = "clear";
pub const DEL_LAST: &str = "undo";
pub const CHANGE_MODE: &str = ":m";
pub const DISPLAY_MODE: &str = ":mode";
pub const PROPOSE_STEP: &str = "propose";
pub const TAKE_STEP: &str = "step";
pub const SHOW_PROGRAM: &str = ":src";
pub const SHOW_ATOMS: &str = ":atoms";
pub const FILTER_ATOMS: &str = ":filter_atoms";
pub const IS_ATOM: &str = ":isatom";
pub const SOE: &str = ":soe";
pub const CONTEXT: &str = ":ctx";
pub const CACHE: &str = "cache";
pub const OPTIMIZATION: &str = "optimization";
pub const SIGNIFICANCE: &str = "sig";
pub const SIGNIFICANCE_PROJECTING: &str = "sig*";
pub const COMPUTE_FACETS_SOE: &str = "!?soe";
pub const MANUAL: &str = "man";
pub const IS_FACET: &str = "isfacet";
pub const IS_FACET_R: &str = "isfacet!";
pub const ENTAILMENT: &str = "|=";
pub const QUIT: &str = ":q";
pub const LOOP: &str = "while";
pub const WHILE_LOOP_DO: &str = "do";
pub const WHILE_LOOP_CMD_SEP: &str = ";";
pub const WHILE_LOOP_VAR_FACETS: &str = "#facets";
pub const WHILE_LOOP_VAR_ROUTE: &str = "#route";
pub const WHILE_LOOP_OP_NEQ: &str = "!=";
pub const WHILE_LOOP_OP_GT: &str = ">";
pub const WHILE_LOOP_OP_GTE: &str = ">=";
pub const WHILE_LOOP_OP_LT: &str = "<";
pub const WHILE_LOOP_OP_LTE: &str = "<=";

// Hard-Coded Aliase für Rückwartskompatibilität
pub const ACTIVATE_FACETS_ALIAS: &str = "+";
pub const ACTIVATE_FACETS_LT_ALIAS: &str = "+'";
pub const ACTIVATE_FACETS_LAZY_ALIAS: &str = ":+";
pub const SHOW_FACETS_ALIAS: &str = "?";
pub const COMPUTE_FACETS_SU_ALIAS: &str = "'!?";
pub const COMPUTE_FACETS_ALIAS: &str = "!?";
pub const FACET_COUNT_ALIAS: &str = "#?";
pub const FACET_COUNTS_ALIAS: &str = "#??";
pub const FACET_COUNTS_PROJECTING_ALIAS: &str = "!#??";
pub const WEIGHTED_FACET_COUNT_ALIAS: &str = "#?w";
pub const WEIGHTED_FACET_COUNTS_ALIAS: &str = "#??w";
pub const ANSWER_SET_COUNT_ALIAS: &str = "#!";
pub const ANSWER_SET_COUNTS_ALIAS: &str = "#!!";
pub const ENUMERATE_SOLUTIONS_ALIAS: &str = "!";
pub const ENUMERATE_PROJECTED_SOLUTIONS_ALIAS: &str = "!*";
pub const SHOW_ROUTE_ALIAS: &str = "@";
pub const CLEAR_ROUTE_ALIAS: &str = "--";
pub const DEL_LAST_ALIAS: &str = "-";
pub const CHANGE_MODE_ALIAS: &str = "'";
pub const PROPOSE_STEP_ALIAS: &str = "$";
pub const TAKE_STEP_ALIAS: &str = "$$";
pub const CONTEXT_ALIAS: &str = ">";
pub const CACHE_ALIAS: &str = ":cache";
pub const OPTIMIZATION_ALIAS: &str = ":opt";
pub const SIGNIFICANCE_ALIAS: &str = "%";
pub const SIGNIFICANCE_PROJECTING_ALIAS: &str = "!%";
pub const IS_FACET_ALIAS: &str = ":?";
pub const IS_FACET_R_ALIAS: &str = ":?r";

pub const FILTER_KEYWORD: &str = "%filter ";
pub const CONTROL_ON: &str = "on";
pub const CONTROL_OFF: &str = "off";
pub const CONTROL_CLEAR: &str = "clear";
pub const CONTROL_SIZE: &str = "size";
pub const CONTROL_STATUS: &str = "status";

pub(crate) fn manual() {
    println!(
        "display facet-inducing atoms                                                                  ->  {SHOW_FACETS}"
    );
    println!(
        "display route                                                                                 ->  {SHOW_ROUTE}"
    );
    println!(
        "enumerate n=[int] answer sets                                                                 ->  {ENUMERATE_SOLUTIONS} n"
    );
    println!(
        "activate facets=[whitespace seperated literals, e.g., a ~b]                                   ->  {ACTIVATE_FACETS} facets"
    );
    println!(
        "activate facets=[whitespace seperated literals, e.g., a ~b] and display consequences          ->  {ACTIVATE_FACETS_LT} facets"
    );
    println!(
        "deactivate previous facet                                                                     ->  {DEL_LAST}"
    );
    println!(
        "deactivate all facets                                                                         ->  {CLEAR_ROUTE}"
    );
    //println!("check whether regex-matched atoms are facets                                                  ->  {IS_FACET} regex");
    //println!("check whether regex-matched atoms are facets with one consistency check                       ->  {IS_FACET_R} regex");
    println!(
        "declare cnf=[e.g., a|~b&c|d] context/query                                                    ->  {CONTEXT} cnf"
    );
    println!(
        "select navigation mode=[{{{{min,max}}#{{f,a,s}}, go}}]                                              ->  {CHANGE_MODE} mode"
    );
    println!(
        "next step in mode                                                                             ->  {PROPOSE_STEP}"
    );
    println!(
        "perform next step in mode                                                                     ->  {TAKE_STEP}"
    );
    println!(
        "compute facets among atoms that match targets=[regex]                                         ->  {COMPUTE_FACETS} targets"
    );
    println!(
        "facet count of facet                                                                          ->  {FACET_COUNT} facet"
    );
    println!(
        "facet counts under each facet filtered from current facets by regex                           ->  {FACET_COUNTS} regex"
    );
    //println!("facet count w.r.t. to provided weights in given filename                                      ->  {WEIGHTED_FACET_COUNT} filename facet");
    //println!("facet counts under each facet w.r.t. to provided regex and weights in given filename          ->  {WEIGHTED_FACET_COUNTS} filename regex");
    println!(
        "facet counts under each facet in targets_1=[regex] using projection on targets_2=[regex]      ->  {FACET_COUNTS_PROJECTING} targets_2 targets_1"
    );
    println!(
        "significance of facets=[regex] for some literal=[a or ~a]                                     ->  {SIGNIFICANCE} literal facets"
    );
    println!(
        "significance of facets=[regex] for some literal=[a or ~a] using projection on targets=[regex] ->  {SIGNIFICANCE_PROJECTING} literal targets facets "
    );
    println!(
        "answer set count                                                                              ->  {ANSWER_SET_COUNT}"
    );
    println!(
        "answer set counts under each facet                                                            ->  {ANSWER_SET_COUNTS}"
    );
    println!(
        "enumerate representative answer sets regarding targets=[regex] filtered from current facets   ->  {SOE} targets"
    );
    println!(
        "display program                                                                               ->  {SHOW_PROGRAM}"
    );
    println!(
        "display atoms                                                                                 ->  {SHOW_ATOMS}"
    );
    println!(
        "display regex-matched atoms                                                                   ->  {FILTER_ATOMS} regex"
    );
    println!(
        "atom check                                                                                    ->  {IS_ATOM}"
    );
    println!(
        "display navigation mode                                                                       ->  {DISPLAY_MODE}"
    );
    println!(
        "control facet cache                                                                            ->  {CACHE} {{{CONTROL_ON},{CONTROL_OFF},{CONTROL_CLEAR},{CONTROL_SIZE},{CONTROL_STATUS}}}"
    );
    println!(
        "control optimized paths                                                                        ->  {OPTIMIZATION} {{{CONTROL_ON},{CONTROL_OFF},{CONTROL_STATUS}}}"
    );
    println!(
        "quit                                                                                          ->  {QUIT}"
    );
    //println!("see documentation for more details");
}
