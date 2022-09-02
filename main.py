import requests
import configparser
import datetime
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    configParser = configparser.RawConfigParser()
    configParser.read("config")
    noteID = configParser["note"]["id"]
    doneDict = {}
    doneList = []
    with open("done.txt", "r") as f:
        doneList = f.readlines()
        for line in doneList:
            line = line.replace("\n", "")
            doneDict[line] = 1
    problemsList = []
    for difficulty, num in dict(configParser["difficulty"].items()).items():
        problems = []
        num = int(num)
        difficulty = str(difficulty)
        while num > 0:
            data = {
                "query": "\n    query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {\n  "
                         "randomQuestion( "
                         "categorySlug: $categorySlug, filters: $filters) {\n    titleSlug\n  }\n}\n    ",
                "variables": {
                    "categorySlug": "algorithms",
                    "filters": {
                        "difficulty": difficulty.upper()
                    }
                }
            }
            r = requests.post("https://leetcode.com/graphql", json=data)
            problemTitle = r.json()["data"]["randomQuestion"]["titleSlug"]
            data = {
                "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: "
                         "QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: "
                         "$categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: "
                         "totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      "
                         "frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      "
                         "status\n "
                         "title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n "
                         "     hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
                "variables": {
                    "categorySlug": "",
                    "skip": 0,
                    "limit": 1,
                    "filters": {
                        "searchKeywords": problemTitle
                    }
                }
            }
            r = requests.post("https://leetcode.com/graphql", json=data)
            question = r.json()["data"]["problemsetQuestionList"]["questions"][0]
            if not question["paidOnly"] and doneDict.get(question["title"]) is None:
                num -= 1
                problems.append((question["title"], question["titleSlug"], question["frontendQuestionId"]))
                if num == 0:
                    problemsList.append(problems)
    token = args.token
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://api.hackmd.io/v1/notes/{noteID}", headers=headers).json()
    r = str(r["content"]).split("##")
    content = r[0]
    content += f"## {datetime.datetime.today().strftime('%Y%m%d')}\n\n"
    for difficulty in problemsList:
        for title, titleSlug, questionId in difficulty:
            content += f"- [{questionId}. {title}](https://leetcode.com/problems/{titleSlug}/)\n"
            doneList.append("\n" + title)
    content += "\n"
    for i in range(1, len(r)):
        content += "##" + r[i]
    data = {"content": content}
    r = requests.patch(f"https://api.hackmd.io/v1/notes/{noteID}", headers=headers, json=data)
    with open("done.txt", "w") as f:
        f.writelines(doneList)
