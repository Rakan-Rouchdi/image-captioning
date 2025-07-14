import sys
import nltk
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
sys.path.append('./pycocoevalcap')
import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import single_meteor_score
from cider.cider import Cider
from bleu.bleu import Bleu

def load_captions(reference_path, generated_path):
    with open(reference_path, 'r') as f:
        references = json.load(f)
    with open(generated_path, 'r') as f:
        generated = json.load(f)
    return references, generated

def evaluate_captions(references, generated):
    smoothie = SmoothingFunction().method4
    bleu_scores = []
    meteor_scores = []
    cider_input = []

    for image_id in generated:
        ref_captions = references.get(image_id, [])
        gen_caption = generated[image_id]

        # BLEU (unigram to 4-gram average)
        bleu = sentence_bleu([r.split() for r in ref_captions], gen_caption.split(), smoothing_function=smoothie)
        bleu_scores.append(bleu)

        # METEOR
        meteor = max(single_meteor_score(ref.split(), gen_caption.split()) for ref in ref_captions)
        meteor_scores.append(meteor)

        # For CIDEr
        cider_input.append((image_id, ref_captions, gen_caption))

    avg_bleu = sum(bleu_scores) / len(bleu_scores)
    avg_meteor = sum(meteor_scores) / len(meteor_scores)

    return avg_bleu, avg_meteor

def evaluate_cider(references, generated):
    # Prepare format for COCO evaluation
    gts = {}
    res = {}
    for img_id in generated:
        gts[img_id] = references.get(img_id, [])
        res[img_id] = [generated[img_id]]

    cider_scorer = Cider()
    score, _ = cider_scorer.compute_score(gts, res)
    return score

if __name__ == "__main__":
    ref_path = "data/captions/references.json"
    gen_path = "data/captions/generated.json"
    references, generated = load_captions(ref_path, gen_path)

    bleu, meteor = evaluate_captions(references, generated)
    cider = evaluate_cider(references, generated)

    print(f"BLEU Score: {bleu:.4f}")
    print(f"METEOR Score: {meteor:.4f}")
    print(f"CIDEr Score: {cider:.4f}")
