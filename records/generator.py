from common.compiler import SUPPORTED_LANGUAGE_SUFFIXES
from common.judge import JudgeResult, judge

from .models import Record


def generate_record(user, problem, compiler, source_code):
    """Generate record from problem and source code."""
    judge_results = judge(
        **_generate_problem_config(
            problem=problem, compiler=compiler, source_code=source_code
        )
    )

    # The result of judge() should never be empty
    # So the following code should be safety
    assert judge_results != []

    accepted_flag = all([result.value == 0 for result in judge_results])

    record = Record(
        user=user,
        problem=problem,
        compiler=compiler,
        source_code=source_code,
        accepted_flag=accepted_flag,
        # TODO Add running time and memory cost
        # running_time = models.DurationField(editable=False)
        # memory_cost = models. ...
    )
    record.save()

    # Add result for per test_case
    if judge_results[0] is JudgeResult.CE:
        _add_ce_result(record)
    else:
        assert len(judge_results) == problem.testcase_set.count()
        _add_results(record, judge_results, problem.testcase_set.all())

    return record


def _add_ce_result(record):
    record.testcaseresult_set.create(
        result_code=JudgeResult.CE.value,
        test_case=None,
    )


def _add_results(record, judge_results, test_cases):
    for result, case in zip(judge_results, test_cases):
        record.testcaseresult_set.create(
            result_code=result.value,
            test_case=case,
        )


def _generate_problem_config(problem, source_code, compiler):
    result = problem.get_problem_config()
    result['source_code'] = source_code
    result['language_suffix'] = \
        SUPPORTED_LANGUAGE_SUFFIXES[compiler][0]
    return result
