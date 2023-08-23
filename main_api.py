import datetime
import os
import pprint
import string
import urllib.request
from typing import Any, List, Optional
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def download_file(url, headers, filename):
    # NOTE the stream=True parameter below
    req = urllib.request.Request(url, headers=headers)

    # headers['content-type'] = 'application/pdf'
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept', 'text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')

    r = urllib.request.urlopen(req).read().decode('utf-8')
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(r)


def get_or_raise(key: str, default: Optional[Any] = None) -> Any:
    value = os.getenv(key)
    if value is None:
        if default:
            return default
        else:
            raise EnvironmentError(f"Missing key: {key}")
    return value


def to_camel(string: str) -> str:
    return "".join(
        word if i == 0 else word.capitalize()
        for i, word in enumerate(string.split("_"))
    )


class ToSnakeCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel


class Status(ToSnakeCaseModel):
    id: str
    name: str
    canonical_name: str


class Answer(ToSnakeCaseModel):
    anni_esperienza_telemarketing: List[str]

    class Config:
        fields = {
            'anni_esperienza_telemarketing': 'CUSTOM_TEXT: Quanti anni hai di esperienza come operatore telemarketing'
        }


class RelevantExperience(ToSnakeCaseModel):
    company: str
    job_title: str


class Candidate(ToSnakeCaseModel):
    candidate_id: str
    job_id: str
    name: str
    location: str
    status_id: str
    degree: str
    field_of_study: str
    requirements_met: int
    requirements: int
    hard_requirements_met: int
    hard_requirements: int
    job_title: str
    last_job_title: str
    last_company: str
    has_cover_letter: bool
    sentiment: str
    answers: Answer
    most_relevant_experience: RelevantExperience
    phone_number: str


class JobInfo(ToSnakeCaseModel):
    job_id: str
    title: str
    status: str


class Response(ToSnakeCaseModel):
    candidates: List[Candidate]
    job_info: List[JobInfo]
    statuses: List[Status]


headers = {
    "authority": "employers.indeed.com",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": get_or_raise("COOKIE"),
    "dnt": "1",
    "indeed-client-application": "entcand",
    "pragma": "no-cache",
    "referer": "https://employers.indeed.com/c",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": get_or_raise("USER_AGENT"),
    "x-datadog-origin": "rum",
    "x-datadog-parent-id": get_or_raise("DATADOG_PARENT_ID"),
    "x-datadog-sampled": "1",
    "x-datadog-sampling-priority": "1",
    "x-datadog-trace-id": get_or_raise("DATADOG_TRACE_ID"),
    "x-indeed-api": "1",
    "x-indeed-appname": "entcand",
    "x-indeed-apptype": "desktop",
    "x-indeed-rpc": "1",
    "x-indeed-tk": get_or_raise("INDEED_TOKEN"),
}

resume_query_params = {
    "id": "{candidate_id}",
    "isPDFView": "true",
    "asText": "false",
    "indeedClientApplication": "candidates-review",
    "indeedcsrftoken": "6OCzZGbA16KNgDDiMRTfhVOLm9TUIfQB"
}

resume_query_string = urlencode(resume_query_params, safe='{}')

base_url = "https://employers.indeed.com/api/ctws/preview/candidates?offset=$offset&encryptedJobId=5c9bdc49aeec&includeOptionalAttributes=true"
# resume_url = "https://employers.indeed.com/c/resume?id={candidate_id}&ctx=&isPDFView=false&asText=false"
# resume_url = "https://employers.indeed.com/api/catws/resume/download?id={candidate_id}&isPDFView=true&asText=false&indeedClientApplication=candidates-review&indeedcsrftoken=6OCzZGbA16KNgDDiMRTfhVOLm9TUIfQB"
resume_url = f"https://employers.indeed.com/api/catws/resume/download?{resume_query_string}"
# POC
download_url = resume_url.format(candidate_id="45515547c96a")

OUTPUT_FILE = "responses.txt"
NOW = datetime.datetime.now()

with open(OUTPUT_FILE, "a") as f:
    f.write(f"{NOW}\n")

more_candidates = True
offset = 0
i = 0

while more_candidates:
    url = string.Template(base_url).substitute(offset=offset)

    r = requests.get(url, headers=headers)
    data = r.json()
    response = Response(**data)

    # pprint.pp(response.candidates)
    candidates = response.candidates
    num_candidates = len(candidates)

    print(f"Found {num_candidates} candidates [round {i + 1}]")

    with open(OUTPUT_FILE, "a") as f:
        pprint.pp(response.json(), f)

    offset += num_candidates
    more_candidates = num_candidates > 0

    for candidate in candidates:
        download_candidate_info_url = resume_url.format(candidate_id=candidate.candidate_id)
        download_file(download_candidate_info_url, headers, f"{candidate.name}_{candidate.candidate_id}.pdf")
        print(f"Downloaded curriculum for {candidate.name}")
        # r = requests.get(download_candidate_info_url, headers=headers)
        # data = r.json()

    i += 1

print(f"Stored {offset} candidates")
