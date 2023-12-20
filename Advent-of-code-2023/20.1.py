import tokenize
from io import BytesIO

data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
# data = open("20.txt").read()

workflows, inputs = data.strip().split("\n\n")
rules_dict: dict[str, "Rule"] = dict()


class Rule:
    def __init__(self, conditions=None) -> None:
        self.var = []
        self.op = []
        self.val = []
        self.res = []
        self.alt = None

        for condition in conditions:
            if len(condition) == 1:
                self.alt = condition[0]
                continue
            # break condition into two
            condition, res = condition
            # save response
            self.res.append(res)
            # save expressions
            for tok in tokenize.tokenize(BytesIO(condition.encode("utf-8")).readline):
                match (tok.type):
                    case tokenize.NAME:
                        self.var.append(tok.string)
                    case tokenize.OP:
                        self.op.append(tok.string)
                    case tokenize.NUMBER:
                        self.val.append(tok.string)

    def match(self, variables):
        # iterate and check if matches
        for var, op, val, res in zip(self.var, self.op, self.val, self.res):
            if var in variables:
                # DEBUG
                # print(
                #     f"expr {var}({variables[var]}) {op} {val} -> {res}",
                #     eval(f"{variables[var]} {op} {val}"),
                # )
                if eval(f"{variables[var]} {op} {val}"):
                    return res
        return self.alt


def resolve(variables):
    res = "in"
    path = [res]
    while res not in ("A", "R"):
        rule = rules_dict[res]
        res = rule.match(variables)
        path.append(res)
    print(path)
    return res


for w in workflows.strip().split("\n"):
    name, conditions = w.split("{")
    conditions = [c.split(":") for c in conditions.strip("}").split(",")]
    rules_dict[name] = Rule(conditions)


tot = 0

for i in inputs.strip().split("\n"):
    variables = {x.split("=")[0]: x.split("=")[1] for x in i[1:-1].split(",")}
    ans = resolve(variables)

    if ans == "A":
        tot += sum(map(int, variables.values()))

print(tot)
