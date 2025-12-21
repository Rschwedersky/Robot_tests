from robot.api import ExecutionResult


result = ExecutionResult('reports/robot/output.xml')
result.configure(stat_config={'suite_stat_level': 2})


failures = []
for test in result.suite.tests:
    if test.status == 'FAIL':
        failures.append({
        'name': test.name,
        'message': test.message,
        'steps': [k.name for k in test.keywords]
        })


# Enviar `failures` para IA para análise
print(failures)