from unittest import TestCase
from molecupy import exceptions
from molecupy.structures import ResiduicStructure, ResiduicSequence, PdbAtom, PdbResidue
from molecupy.structures import _residue_id_to_int

class ResiduicSequenceTest(TestCase):

    def setUp(self):
        self.atom1 = PdbAtom(1.0, 1.0, 1.0, "H", 1, "H1")
        self.atom2 = PdbAtom(1.0, 1.0, 2.0, "C", 2, "CA")
        self.atom3 = PdbAtom(1.0, 1.0, 3.0, "O", 3, "OX1")
        self.residue1 = PdbResidue("A1", "ARG", self.atom1, self.atom2, self.atom3)
        self.atom4 = PdbAtom(1.0, 1.0, 4.0, "H", 4, "H1")
        self.atom5 = PdbAtom(1.0, 1.0, 5.0, "C", 5, "CA")
        self.atom6 = PdbAtom(1.0, 1.0, 6.0, "O", 6, "OX1")
        self.residue2 = PdbResidue("A2", "HIS", self.atom4, self.atom5, self.atom6)
        self.atom7 = PdbAtom(1.0, 1.0, 7.0, "H", 7, "H1")
        self.atom8 = PdbAtom(1.0, 1.0, 8.0, "C", 8, "CA")
        self.atom9 = PdbAtom(1.0, 1.0, 9.0, "O", 9, "OX1")
        self.residue3 = PdbResidue("A3", "TRP", self.atom7, self.atom8, self.atom9)


    def check_valid_residuic_sequence(self, residuic_sequence):
        self.assertIsInstance(residuic_sequence, ResiduicSequence)
        self.assertIsInstance(residuic_sequence, ResiduicStructure)
        self.assertIsInstance(residuic_sequence.residues, list)
        for residue in residuic_sequence.residues:
            self.assertIsInstance(residue, PdbResidue)
        self.assertRegex(str(residuic_sequence), r"<ResiduicSequence \((\d+) residues\)>")



class ResiduicStructureCreationTests(ResiduicSequenceTest):

    def test_can_create_residuic_sequence(self):
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.check_valid_residuic_sequence(residuic_sequence)


    def test_residues_are_ordered(self):
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.assertEqual(
         residuic_sequence.residues,
         [self.residue1, self.residue2, self.residue3]
        )
        residuic_sequence = ResiduicSequence(self.residue3, self.residue1, self.residue2)
        self.assertEqual(
         residuic_sequence.residues,
         [self.residue1, self.residue2, self.residue3]
        )



class ResduicSequenceGenerationTests(ResiduicSequenceTest):

    def test_can_get_protein_sequence(self):
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.assertEqual(
         residuic_sequence.get_sequence_string(),
         "RHW"
        )


    def test_can_get_protein_sequence_with_unknown_residues(self):
        self.residue2.residue_name = "ABC"
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.assertEqual(
         residuic_sequence.get_sequence_string(),
         "RXW"
        )



class ResiduicSequenceOrderingTests(ResiduicSequenceTest):

    def test_residue_id_int_conversion(self):
        self.assertEqual(_residue_id_to_int("A1"), 100)
        self.assertEqual(_residue_id_to_int("B1"), 100)
        self.assertEqual(_residue_id_to_int("A2"), 200)
        self.assertEqual(_residue_id_to_int("A100"), 10000)
        self.assertEqual(_residue_id_to_int("A1A"), 101)
        self.assertEqual(_residue_id_to_int("A1B"), 102)
        self.assertEqual(_residue_id_to_int("B1A"), 101)
        self.assertEqual(_residue_id_to_int("B1B"), 102)
        self.assertEqual(_residue_id_to_int("G1009Q"), 100917)


    def test_can_handle_insert_codes(self):
        self.residue1.residue_id = "D1001C"
        self.residue2.residue_id = "D1001"
        self.residue3.residue_id = "D1001B"
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.assertEqual(
         residuic_sequence.residues,
         [self.residue2, self.residue3, self.residue1]
        )


    def test_ordering_is_numeric(self):
        self.residue1.residue_id = "A30"
        self.residue2.residue_id = "A200"
        self.residue3.residue_id = "A1000"
        residuic_sequence = ResiduicSequence(self.residue1, self.residue2, self.residue3)
        self.assertEqual(
         residuic_sequence.residues,
         [self.residue1, self.residue2, self.residue3]
        )