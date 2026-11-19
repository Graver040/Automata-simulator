from itertools import product
import unittest

from src import mealy_to_moore, moore_to_mealy
from src.examples import MEALY, MOORE
from src.parser import parse
from src.simulator import aligned, simulate, tokenize
from src.validator import validate


class ConversionTests(unittest.TestCase):
    def test_mealy_sample(self):
        original = parse("Mealy", *MEALY)
        result, pairs = mealy_to_moore.convert(original)
        validate(result)
        self.assertEqual(result.initial, "S")
        self.assertEqual(pairs, {"A_0": ("A", "0"), "A_1": ("A", "1"),
                                 "B_0": ("B", "0"), "B_1": ("B", "1")})
        self.assertEqual(result.state_outputs, {"S": None, "A_0": "0", "A_1": "1",
                                                "B_0": "0", "B_1": "1"})
        expected = {"S": ("B_0", "A_1"), "A_0": ("B_0", "A_1"),
                    "A_1": ("B_0", "A_1"), "B_0": ("A_0", "B_1"), "B_1": ("A_0", "B_1")}
        for state, destinations in expected.items():
            self.assertEqual(tuple(result.transitions[state, a] for a in ("0", "1")), destinations)
        trace = simulate(result, list("01"))
        self.assertEqual(trace.raw, [None, "0", "1"])
        self.assertEqual([step[2] for step in trace.steps], ["B_0", "B_1"])
        self.assertEqual(aligned(result, trace), simulate(original, list("01")).raw)

    def test_moore_sample(self):
        original = parse("Moore", *MOORE)
        result = moore_to_mealy.convert(original)
        validate(result)
        self.assertEqual(result.initial, "A")
        self.assertEqual(result.transitions, original.transitions)
        self.assertEqual(result.edge_outputs,
                         {("A", "0"): "1", ("A", "1"): "0", ("B", "0"): "0", ("B", "1"): "1"})
        trace = simulate(original, list("01"))
        self.assertEqual(trace.raw, list("011"))
        self.assertEqual(simulate(original, list("00")).raw, list("010"))
        self.assertEqual(simulate(result, list("00")).raw, list("10"))
        self.assertEqual(aligned(original, trace), simulate(result, list("01")).raw)

    def test_same_output_and_unreachable(self):
        original = parse("Mealy", "A,U", "0,1", "red,blue", "A",
                         "A,0,A,red\nA,1,A,red\nU,0,U,blue\nU,1,U,blue")
        result, pairs = mealy_to_moore.convert(original)
        self.assertEqual(pairs, {"A_red": ("A", "red")})
        self.assertEqual(len(result.states), 2)

    def test_label_collisions(self):
        original = parse("Mealy", "S,A_x,A", "0,1", "y,x_y", "S",
                         "S,0,A_x,y\nS,1,A,x_y\nA_x,0,A_x,y\nA_x,1,A,x_y\nA,0,A_x,y\nA,1,A,x_y")
        result, pairs = mealy_to_moore.convert(original)
        validate(result)
        self.assertNotEqual(result.initial, "S")
        self.assertEqual(len(pairs), 2)
        self.assertEqual(set(pairs.values()), {("A_x", "y"), ("A", "x_y")})
        self.assertEqual(simulate(result, list("01")).raw, [None, "y", "x_y"])

    def test_all_sample_words_through_length_four(self):
        mealy = parse("Mealy", *MEALY)
        moore = parse("Moore", *MOORE)
        for original, result in ((mealy, mealy_to_moore.convert(mealy)[0]),
                                 (moore, moore_to_mealy.convert(moore))):
            for length in range(5):
                for word in product(original.inputs, repeat=length):
                    with self.subTest(kind=original.kind, word=word):
                        self.assertEqual(aligned(original, simulate(original, list(word))),
                                         aligned(result, simulate(result, list(word))))

    def test_multicharacter_symbols_and_empty_input(self):
        original = parse("Mealy", "A", "go,stop", "red,green", "A", "A,go,A,green\nA,stop,A,red")
        result, _ = mealy_to_moore.convert(original)
        self.assertEqual(simulate(result, []).raw, [None])
        self.assertEqual(simulate(original, []).raw, [])
        self.assertEqual(aligned(result, simulate(result, tokenize(" go  stop ", result.inputs))),
                         ["green", "red"])
        with self.assertRaisesRegex(ValueError, "position 2"):
            simulate(original, ["go", "unknown"])


class ValidationTests(unittest.TestCase):
    def test_bad_mealy_definitions(self):
        cases = (
            (4, "A,0,B,0", "Missing transition"),
            (4, MEALY[4] + "\nA,0,B,0", "Duplicate transition"),
            (4, MEALY[4].replace("A,0,B,0", "A,0,C,0"), "Unknown destination"),
            (4, MEALY[4].replace("A,0,B,0", "A,0,B,9"), "Unknown output"),
            (4, MEALY[4].replace("A,0,B,0", "A,9,B,0"), "Undeclared"),
            (3, "C", "Unknown initial"),
            (2, "0,1,ε", "reserved"),
            (0, "A,A,B", "duplicate"),
            (1, "", "nonempty"),
        )
        for index, replacement, expected in cases:
            arguments = list(MEALY)
            arguments[index] = replacement
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, expected):
                parse("Mealy", *arguments)

    def test_missing_moore_output(self):
        with self.assertRaisesRegex(ValueError, "one output per declared state"):
            parse("Moore", *MOORE[:-1], "A,0")
