import tokenize
from io import BytesIO
import itertools

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
data = open("20.txt").read()

workflows, inputs = data.strip().split("\n\n")
rules_dict: dict[str, "RuleSet"] = dict()


class Rule:
    def __init__(self, var, op, val, res) -> None:
        self.var = var
        self.op = op
        self.val = int(val)
        self.res = res

    def get_var_bounds(self):
        start = 0
        end = 4001
        if self.op == ">":
            start = self.val
        elif self.op == "<":
            end = self.val
        return (start, end)

    def get_inverse(self):
        if self.op == ">":
            return Rule(self.var, "<", self.val + 1, "~" + self.res)
        else:
            return Rule(self.var, ">", self.val - 1, "~" + self.res)

    def is_non_contradicting(self, others: list["Rule"]):
        for other in others:
            var, op, val = other.var, other.op, other.val
            # not same variable (x, a) or if has same operator (x>100 and x>1000)
            if var != self.var or op == self.op:
                continue
            # same variable and different operator must be x < A, x > B form
            else:
                if self.op == "<" and self.val > val:
                    continue
                elif self.op == ">" and self.val < val:
                    continue
            return False
        return True

    def print(self):
        return f"{self.var} {self.op} {self.val}"


class RuleSet:
    def __init__(self, conditions=None) -> None:
        self.rules: list[Rule] = []
        self.alt: str = None

        for condition in conditions:
            if len(condition) == 1:
                self.alt = condition[0]
                continue
            # break condition into two
            condition, res = condition
            # save expressions
            var, op, val = None, None, None
            for tok in tokenize.tokenize(BytesIO(condition.encode("utf-8")).readline):
                match (tok.type):
                    case tokenize.NAME:
                        var = tok.string
                    case tokenize.OP:
                        op = tok.string
                    case tokenize.NUMBER:
                        val = tok.string
            self.rules.append(Rule(var, op, val, res))

    def print(self):
        return ", ".join([r.print() for r in self.rules])


for w in workflows.strip().split("\n"):
    name, conditions = w.split("{")
    conditions = [c.split(":") for c in conditions.strip("}").split(",")]
    rules_dict[name] = RuleSet(conditions)


def get_rule_intersection_size(rules: list["Rule"]):
    var_mins = {v: 0 for v in "xmas"}
    var_maxs = {v: 4001 for v in "xmas"}
    paths = 1

    for rule in rules:
        v = rule.var
        s, e = rule.get_var_bounds()
        var_mins[v] = max(var_mins[v], s)
        var_maxs[v] = min(var_maxs[v], e)
    for v in "xmas":
        if var_maxs[v] - var_mins[v] < 0:
            return 0
        paths *= var_maxs[v] - var_mins[v] - 1

    return paths


path_names: list[list[str]] = []
paths_rules: list[list[Rule]] = []


def recursive_resolve(res=["in"], path=[]):
    curr_res = res[-1]
    if curr_res in ("A", "R"):
        global path_names, paths_rules
        path_names.append(res)
        paths_rules.append(path)
        return res

    rule_set = rules_dict[curr_res]
    negated = []
    for rule in rule_set.rules:
        if rule.is_non_contradicting(path) or True:
            new_res = res + [rule.res]
            new_path = path + negated + [rule]
            recursive_resolve(new_res, new_path)
        negated.append(rule.get_inverse())
    new_res = res + [rule_set.alt]
    new_path = path + negated
    recursive_resolve(new_res, new_path)


recursive_resolve()
paths_rules_accepted = []
for names, rules in zip(path_names, paths_rules):
    if names[-1] == "R":
        continue
    paths_rules_accepted.append(rules)

tot = 0
for rules in paths_rules_accepted:
    tot += get_rule_intersection_size(rules)

print(tot)
