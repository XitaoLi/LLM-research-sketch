import json
import os
from typing import List
import numpy as np


class FED_PMT:
    def independence(factor, dialogue, max_score):
        if factor == "Depth":
            return f"Dialogue:\n{dialogue}\nEvaluation:\nScore from 0 to {max_score-1} for the dialogue according to the depth of discussion topics (Integer ONLY).\nOutput format is <num>\nOutput:"
        elif factor == "Overall": 
            return f"Dialogue:\n{dialogue}\nEvaluation:\nScore from 0 to {max_score-1} for the dialogue according to the overview impression of the dialogue quality (Integer ONLY).\nOutput format is <num>\nOutput:"
    
    def independence_fine_grained(factor, dialogue, max_score):
        if factor == "Depth":
            return f"Dialogue:\n{dialogue}\nEvaluation:\nScore from 0.0 to {max_score}.0 for the dialogue according to the depth of discussion topics.\nOutput format is <num>.<num> (such as 3.2, 1.7, 4.9)\nOutput:"
        elif factor == "Overall": 
            return f"Dialogue:\n{dialogue}\nEvaluation:\nScore from 0.0 to {max_score}.0 for the dialogue according to the overview impression of the dialogue quality.\nOutput format is <num>.<num> (such as 3.2, 1.7, 4.9)\nOutput:"

    def demo(factor,scale):
        with open("dataset/fed-dial_eval.json") as f:
            data = json.load(f)
        # scale = 5
        evaluator_num = 5
        demo_str = "Demonstractions of human evaluators:"
        demo_ids = []
        for target in range(scale):
            success_falg = False
            for target_freq in range(evaluator_num-1, -1, -1):
                for i,item in enumerate(data):
                    human_score = np.array(item["annotations"][factor])
                    if np.sum(human_score==target) == target_freq:
                        dialogue = item["dialog"]
                        dialogue_str = ""
                        for turn in dialogue:
                            dialogue_str += f"{turn['speaker']}:{turn['text']}\n"
                        demo_str += f"\n<Dialogue>\n{dialogue_str[:-1]}\n<human scores>\n{human_score}\n"
                        demo_ids.append(i)
                        success_falg = True
                        break
                if success_falg: break

        print("Demos idx: ",demo_ids)
        return demo_str

    def compare(dia1:str,dia2:List[str]):
        reference = "\n".join(dia2)
        return \
f"""The following references are scored under the equal criterial. People evaluators think they can be scored same according to the overview impression of the dialogue quality .

References:
{reference}

Now as a evaluator, evaluate the dialogue according to the overview impression of the dialogue quality.
Dialogue:
{dia1}

What's the overview impression of the dialogue quality compared with  the references?
A. better than references
B. worse than references
C. same with references

Your judge (LABEL ONLY):
"""

    def compare2(dia1:str,dia2:List[str]):
        reference = "\n".join(dia2)
        return \
f"""The following references are scored under the equal criterial. People evaluators think they can be scored same according to the overview impression of the dialogue quality .

References:
{reference}

Now as a evaluator, evaluate the dialogue according to the overview impression of the dialogue quality.
Dialogue:
{dia1}

What's the overview impression of the dialogue quality compared with  the references?
A. better than references
B. worse than references

Your judge (LABEL ONLY):
"""
    def compare3(dia1:str,dia2:str):
        return \
f"""The following references are scored under the equal criterial. People evaluators think they can be scored same according to the overview impression of the dialogue quality .

References:
{dia2}

Now as a evaluator, evaluate the dialogue according to the overview impression of the dialogue quality.
Dialogue:
{dia1}

What's the overview impression of the dialogue quality compared with  the references?
A. better than references
B. worse than references

Your judge (LABEL ONLY):
"""

    def scale(dialogue):
        return \
"""A Likert scale is a psychometric scale commonly used in questionnaires to measure people's attitudes, opinions, or perceptions. The following 10-question Likert scale can be used to evaluate the quality of a dialogue:

Dialogue to be evaluated:
{dialogue}

Please rate the following statements on a scale of 1 to 5, where 1 = strongly disagree, 2 = disagree, 3 = neutral, 4 = agree, and 5 = strongly agree.
1.The dialogue had a clear and engaging topic.
2.The conversation flowed naturally and smoothly.
3.Both participants in the dialogue expressed their ideas and opinions clearly.
4.The dialogue demonstrated an appropriate level of depth and complexity.
5.The participants in the dialogue listened and responded to each other effectively.
6.The dialogue was coherent, with each statement building on the previous one.
7.The participants in the dialogue used appropriate language and tone for the context.
8.The dialogue maintained a consistent focus on the topic throughout the conversation.
9.The participants in the dialogue demonstrated mutual respect and understanding.
10.Overall, the quality of the dialogue was high and met the expectations of the evaluators.

Output your answers in json format \{"question1":<scale1>,"question2":<scale2>,...,"question10":<scale10>\}

Outputs:"""

class Comparison:
    def direct_compare(dia1,dia2,factor):
        #overview impression of the dialogue quality
        factor_interpret = factor
        return \
f"""[Dialogue 1]
{dia1}
[Dialogue 2]
{dia2}
[System]
We would like to request your to act as a evaluator, evaluate the dialogue according to the {factor_interpret}.
Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment. Then, output one line indicating which is better. Output with the following format: 
Evaluation evidence: <evaluation explanation here>
The winner: <dialogue1> or <dialogue2>"""
    def score_compare(dia1,dia2,factor):
        factor_interpret = factor
        return \
f"""[Dialogue 1]
{dia1}
[Dialogue 2]
{dia2}
[System]
We would like to request your to act as a evaluator, evaluate the dialogue according to the {factor_interpret}. Each dialogue receives an overall score on a scale of 1 to 5, where a higher score indicates better overall performance.
Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment. Then, output two lines indicating the scores for Dialogue 1 and 2, respectively. Output with the following format: 
Evaluation evidence: <evaluation explanation here>
The score of Dialogue 1: <score>
The score of Dialogue 2: <score>"""


        