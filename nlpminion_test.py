import unittest
from feature_vector import FeatureVector
from adadelta import Adadelta
import decoder
import os
from translation import Translation


class TestNLPminion(unittest.TestCase):
    '''Runs some basic unit tests to check if everything works.

    Requires the decoder_path variable set to the location of the top level directory of cdec
    '''

    decoder_path = "/toolbox/cdec/"

    def test_adadelta(self):
        '''Using a gradient with two dimensions to test if the adadelta update works.

         Adadelta algorithm as described in (Zeiler, 2013).
         The test passes if the delta values are correct.
        '''
        adadelta = Adadelta()
        true_delta = FeatureVector()
        true_delta.from_string("test1=0.004472133120656804 test2=-0.0044721287995992225")
        gradient = FeatureVector()
        gradient.from_string("test1=-3.9722 test2=2.5")
        test_delta = adadelta.update(gradient)
        self.assertEqual(true_delta, test_delta)

    def test_persentence_bleu(self):
        '''For a few special cases the per sentence BLEU values (Nakov et al, 2012) are computed and verified.'''
        # general test for 1-gram and 4-gram
        sent = "at how many places can i go climbing in paris ?"
        ref = "in how many spots can i go climbing in paris ?"
        self.assertEqual(decoder.per_sentence_bleu(sent, [ref], 1), 0.8181818181818182)
        self.assertEqual(decoder.per_sentence_bleu(sent, [ref], 4), 0.667354307257489)
        # test several references
        sent = "at how many places can i go climbing in paris ?"
        ref = ["in how many spots can i go climbing in paris ?", "in how many places can i go climbing in paris ?"]
        self.assertEqual(decoder.per_sentence_bleu(sent, ref, 1), 0.9090909090909092)
        # test BLEU=0
        sent = "this is a completely different string !"
        ref = "in how many spots can i go climbing in paris ?"
        self.assertEqual(decoder.per_sentence_bleu(sent, [ref], 1), 0.0)
        # test clipping
        sent = "in in how many places can i go climbing in paris ?"
        ref = "in how many spots can i go climbing in paris ?"
        self.assertEqual(decoder.per_sentence_bleu(sent, [ref], 1), 0.8333333333333335)

    def test_decoder_pipeline(self):
        '''Checks if the decoding procedures work without issues.

        It tests both passing a file to cdec and passing an input string. Further tests cdec's corpus BLEU and
        the conversion of cdec's returned features to a FeatureVector object
        '''
        translation_out = open("decoder_test/output-translation.tmp", 'w')
        print >> translation_out, decoder.translate("%s/decoder/cdec" % self.decoder_path, "decoder_test/cdec.ini",
                                                "decoder_test/weights.init", "decoder_test/set.in").strip()
        translation_out.close()
        bleu = decoder.bleu("%s/mteval/fast_score" % self.decoder_path, "decoder_test/set.ref",
                            "decoder_test/output-translation.tmp").strip()
        os.remove("decoder_test/output-translation.tmp")
        self.assertEqual(bleu, '0.296757')
        translation_out = open("decoder_test/output-translation.tmp", 'w')
        sentence = '<seg grammar="decoder_test/grammar.1" id="1"> wo in edinburgh gibt es restaurants in denen das rauchen nicht erlaubt ist ? </seg>'
        print >> translation_out, decoder.translate_sentence("%s/decoder/cdec" % self.decoder_path,
                                  "decoder_test/cdec.ini", "decoder_test/weights.init", sentence).strip()
        translation_out.close()
        bleu = decoder.bleu("%s/mteval/fast_score" % self.decoder_path, "decoder_test/sentence.ref",
                            "decoder_test/output-translation.tmp").strip()
        os.remove("decoder_test/output-translation.tmp")
        self.assertEqual(bleu, '0.465954')
        translation_raw = decoder.translate_sentence("%s/decoder/cdec" % self.decoder_path,
                          "decoder_test/cdec.ini", "decoder_test/weights.init", sentence, 2).strip()
        translation = Translation(translation_raw.split("\n")[0])
        self.assertEqual(translation.idval, '1')
        self.assertEqual(translation.string, "where there are restaurants in edinburgh where smoking is not allowed ?")
        self.assertEqual(translation.decoder_score, -4.73151)

if __name__ == '__main__':
    unittest.main()