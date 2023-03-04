import requests
import configparser
import datetime
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--note", required=True)
    parser.add_argument("--webhook")
    args = parser.parse_args()
    configParser = configparser.RawConfigParser()
    configParser.read("config")
    noteID = args.note
    token = args.token
    webhook = args.webhook
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
                "query": "query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {"
                         "randomQuestion(categorySlug: $categorySlug, filters: $filters) {titleSlug}}",
                "variables": {
                    "categorySlug": "algorithms",
                    "filters": {
                        "difficulty": difficulty.upper()
                    }
                }
            }
            r = requests.post("https://leetcode.com/graphql", json=data)
            problemTitle = r.json()["data"]["randomQuestion"]["titleSlug"]
            data = {"operationName": "questionData",
                    "variables": {"titleSlug": problemTitle},
                    "query": "query questionData($titleSlug: String!) {question(titleSlug: $titleSlug) {likes, "
                             "dislikes, questionFrontendId, isPaidOnly, title}}"}
            r = requests.post("https://leetcode.com/graphql", json=data)
            question = r.json()["data"]["question"]
            likes = question["likes"]
            dislikes = question["dislikes"]
            if not question["isPaidOnly"] and doneDict.get(question["title"]) is None and likes > dislikes:
                num -= 1
                problems.append((question["title"], problemTitle, question["questionFrontendId"]))
                if num == 0:
                    problemsList.append(problems)
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
    problemDescription = ""
    for difficulty in problemsList:
        for title, titleSlug, questionId in difficulty:
            problemDescription += f"{questionId}. {title}\n"
    data = {"embeds": [{"description": problemDescription, "title": datetime.datetime.today().strftime('%Y%m%d')}]}
    if webhook is not None:
        requests.post(f"https://discord.com/api/webhooks/{webhook}", json=data)
