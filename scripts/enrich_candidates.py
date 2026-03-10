#!/usr/bin/env python3

import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/candidates.json"
LAST_UPDATED = "2026-03-10"
REQ_HEADERS = {"User-Agent": "Mozilla/5.0"}
SOCIAL_SWEEP_PATH = ROOT / "scripts/social_sweep_updates.json"


RESEARCH_UPDATES = json.loads(
    r'''
{
  "indira-rana-magar": {
    "socials": [
      { "platform": "Website", "url": "https://indiraranamagar.com/" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://indiraranamagar.com/" },
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Indira_Rana_Magar" }
    ]
  },
  "sobita-gautam": {
    "education": [
      { "level": "Bachelors", "degree": "Law" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sobita-gautam" }
    ]
  },
  "lekh-jung-thapa": {
    "education": [
      { "level": "Masters", "degree": "MD in Internal Medicine" },
      { "level": "Other", "degree": "DM in Neurology" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/dr-lekhjung-thapa" }
    ]
  },
  "sulav-kharel": {
    "education": [
      { "level": "+2", "degree": "Science" },
      {
        "level": "Bachelors",
        "degree": "BA LL.B.",
        "institution": "Nepal Law Campus",
        "country": "Nepal"
      },
      { "level": "Masters", "degree": "Constitutional Law", "country": "United States" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sulabha-kharel" }
    ]
  },
  "rubina-acharya": {
    "education": [
      {
        "level": "+2",
        "institution": "Maryland College, Biratnagar",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "degree": "MBA",
        "institution": "Kathmandu University",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/rubina-acharya" }
    ]
  },
  "badan-kumar-bhandari": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "BA",
        "institution": "Kailashkut Multiple Campus",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/badan-kumar-bhandari" }
    ]
  },
  "rajan-gautam": {
    "education": [
      { "level": "Masters", "degree": "Education, Management, and Political Science" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/rajan-gautam-1" }
    ]
  },
  "nisha-dangi": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "Social Work",
        "institution": "Jaya Multiple Campus",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "degree": "Journalism",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/nisha-dangi" }
    ]
  },
  "narendra-kumar-gupta": {
    "education": [
      { "level": "Bachelors", "degree": "Management" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/narendra-kumar-gupta" }
    ]
  },
  "kamal-subedi": {
    "education": [
      {
        "level": "SLC",
        "institution": "Birendra Secondary School, Hekuli",
        "country": "Nepal"
      },
      {
        "level": "+2",
        "institution": "Gyan Sindhu Higher Secondary School",
        "country": "Nepal"
      },
      {
        "level": "Bachelors",
        "degree": "Education",
        "institution": "Mahendra Ratna Campus, Tahachal",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      },
      {
        "level": "Other",
        "degree": "Diploma in Development Leadership",
        "country": "Canada"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/kamal-subedi" }
    ]
  },
  "bipin-kumar-acharya": {
    "education": [
      {
        "level": "SLC",
        "institution": "Dipshikha Residential School",
        "country": "Nepal"
      },
      {
        "level": "Bachelors",
        "degree": "Biotech Engineering",
        "country": "India"
      },
      { "level": "Masters", "degree": "Management" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/bipin-kumar-acharya" }
    ]
  },
  "toshima-karki": {
    "socials": [
      { "platform": "Website", "url": "https://toshimakarki.com/" }
    ],
    "education": [
      {
        "level": "SLC",
        "institution": "Shahid Dharmabhakta School, Nakkhu",
        "country": "Nepal"
      },
      {
        "level": "+2",
        "institution": "Modern Indian School, Chobhar",
        "country": "Nepal"
      },
      {
        "level": "Bachelors",
        "degree": "MBBS",
        "institution": "KIST Medical College, Lalitpur",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "degree": "MS in General Surgery",
        "institution": "Kathmandu University",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://toshimakarki.com/about-me/" },
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Toshima_Karki" },
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/tosima-karki" }
    ]
  },
  "devaraj-pathak": {
    "education": [
      {
        "level": "SLC",
        "institution": "Shree Madhyamik Vidyalaya, Bangaun Deukhuri",
        "country": "Nepal"
      },
      { "level": "Bachelors", "degree": "Commerce" },
      { "level": "Masters", "degree": "Sociology" },
      { "level": "Masters", "degree": "Social Values" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/devraj-pathak" }
    ]
  },
  "manish-khanal": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "Law",
        "institution": "Nepal Law Campus",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/manish-khanal" }
    ]
  },
  "jagdish-kharel": {
    "socials": [
      { "platform": "Website", "url": "https://jagdishkharel.com.np" },
      { "platform": "Facebook", "url": "https://www.facebook.com/jagdish.kharel.5/" }
    ],
    "education": [
      {
        "level": "Masters",
        "degree": "Mass Communication",
        "institution": "Tribhuvan University"
      }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://jagdishkharel.com.np" },
      { "platform": "Facebook", "url": "https://www.facebook.com/jagdish.kharel.5/" },
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Jagdish_Kharel" }
    ]
  },
  "ashika-tamang": {
    "socials": [
      { "platform": "Facebook", "url": "https://www.facebook.com/ashikatamangofficial/" }
    ],
    "sources": [
      { "platform": "Facebook", "url": "https://www.facebook.com/ashikatamangofficial/" }
    ]
  },
  "swarnim-wagle": {
    "socials": [
      { "platform": "Website", "url": "https://swarnimwagle.com.np" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://swarnimwagle.com.np" }
    ]
  },
  "sitaram-sah": {
    "education": [
      { "level": "Bachelors", "degree": "Soil Conservation" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.ekantipur.com/profile/576?lng=eng" }
    ]
  },
  "rukesh-ranjit": {
    "socials": [
      { "platform": "Facebook", "url": "https://www.facebook.com/rukesh.ranjit.rsp/" }
    ],
    "education": [
      { "level": "Masters", "degree": "MBA" }
    ],
    "sources": [
      { "platform": "Facebook", "url": "https://www.facebook.com/rukesh.ranjit.rsp/" },
      { "platform": "News Article", "url": "https://election.ekantipur.com/profile/1584?lng=eng" }
    ]
  },
  "dipak-kumar-sah": {
    "education": [
      {
        "level": "Masters",
        "degree": "Public Health",
        "institution": "London School of Hygiene & Tropical Medicine; Institute of Medicine"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/dipaka-kumara-saha-1" }
    ]
  },
  "ananda-bahadur-chand": {
    "education": [
      { "level": "Masters", "degree": "Biochemistry" },
      { "level": "PhD" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/ananda-bahadur-chand" }
    ]
  },
  "sasmit-pokharel": {
    "education": [
      { "level": "+2", "degree": "A Levels", "country": "United States" },
      {
        "level": "Bachelors",
        "degree": "BALLB",
        "institution": "Kathmandu University School of Law"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sasmit-pokharel" }
    ]
  },
  "prashant-upreti": {
    "education": [
      { "level": "Bachelors", "degree": "Tourism Management" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/prashant-upreti" }
    ]
  },
  "sudhan-gurung": {
    "education": [
      { "level": "+2", "degree": "A Levels", "institution": "Multi International College" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sudhan-gurung" }
    ]
  },
  "sagar-dhakal": {
    "education": [
      { "level": "Masters", "degree": "MSc", "institution": "Oxford University" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sagar-dhakal" }
    ]
  },
  "madhukumar-chaulagain": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "Law",
        "institution": "Nepal Law Campus, Tribhuvan University"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/madhu-kumar-chaulagai" }
    ]
  },
  "khagendra-sunar": {
    "education": [
      { "level": "Bachelors", "degree": "Political Science and History" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/khagendra-sunar" }
    ]
  },
  "pukar-bam": {
    "education": [
      { "level": "Masters", "degree": "Sociology" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/pukar-bam" }
    ]
  },
  "dhannjaya-regmi": {
    "education": [
      { "level": "PhD", "degree": "Environmental Earth Science", "institution": "Hokkaido University" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/dhannjaya-regmi" }
    ]
  },
  "ramji-yadav": {
    "education": [
      { "level": "Bachelors", "degree": "BE in Electrical Engineering" }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/ramji-yadav" }
    ]
  },
  "tek-bahadur-shakya": {
    "education": [
      {
        "level": "Intermediate",
        "degree": "Proficiency Certificate",
        "institution": "Thakur Ram Multiple Campus"
      }
    ],
    "sources": [
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/tek-bahadur-shakya" }
    ]
  },
  "shishir-khanal": {
    "socials": [
      { "platform": "Website", "url": "https://shisirkhanal.com" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "BA in IPED",
        "institution": "University of Bridgeport"
      },
      {
        "level": "Masters",
        "degree": "Master of International Public Affairs (MIPA)",
        "institution": "University of Wisconsin-Madison"
      }
    ],
    "sources": [
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Shishir_Khanal" },
      { "platform": "Official Website", "url": "https://shisirkhanal.com" },
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/shishir-khanal" }
    ]
  },
  "sushant-vaidik": {
    "socials": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/sushant-vaidik" },
      { "platform": "Facebook", "url": "https://www.facebook.com/Sushant4Pyuthan/" }
    ],
    "education": [
      {
        "level": "Masters",
        "degree": "MSc Economics",
        "institution": "London School of Economics and Political Science",
        "country": "United Kingdom"
      }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://iidglobal.org/our-experts/" },
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/sushant-vaidik" },
      { "platform": "Facebook", "url": "https://www.facebook.com/Sushant4Pyuthan/" }
    ]
  },
  "biraj-bhakta-shrestha": {
    "socials": [
      { "platform": "Website", "url": "https://birajbhakta.com.np/" },
      { "platform": "Facebook", "url": "https://www.facebook.com/Birajleads/" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://birajbhakta.com.np/" },
      { "platform": "Facebook", "url": "https://www.facebook.com/Birajleads/" },
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Biraj_Bhakta_Shrestha" }
    ]
  },
  "janak-singh-dhami": {
    "socials": [
      { "platform": "Facebook", "url": "https://www.facebook.com/janak.dhami.7547/" }
    ],
    "sources": [
      { "platform": "Facebook", "url": "https://www.facebook.com/janak.dhami.7547/" }
    ]
  },
  "bikram-timilsina": {
    "socials": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/bikram-timilsina" },
      { "platform": "Facebook", "url": "https://www.facebook.com/bikramtimilsina/" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "English and Economics",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "degree": "Master of International Studies (Advanced)",
        "institution": "The University of Queensland",
        "country": "Australia"
      },
      {
        "level": "Masters",
        "degree": "English Language and Literature",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      },
      {
        "level": "PhD",
        "degree": "Politics and International Relations",
        "institution": "Griffith University",
        "country": "Australia"
      }
    ],
    "sources": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/bikram-timilsina" },
      { "platform": "Official Website", "url": "https://www.aifar.org.np/aifar-member/dr-bikram-timilsina-research" }
    ]
  },
  "sushil-khadka": {
    "socials": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/sushil-khadka-28901929" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "Biological Engineering",
        "institution": "University of Maine",
        "country": "United States"
      },
      {
        "level": "Masters",
        "degree": "Economic Development",
        "institution": "Vanderbilt University",
        "country": "United States"
      }
    ],
    "sources": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/sushil-khadka-28901929" },
      { "platform": "Official Website", "url": "https://avnicenter.org/team/sushil-khadka/" }
    ]
  },
  "tara-prasad-joshi": {
    "socials": [
      { "platform": "Website", "url": "https://tarajoshi.com.np/" },
      { "platform": "Facebook", "url": "https://www.facebook.com/profile.php?id=100086656631042" }
    ],
    "education": [
      { "level": "Bachelors", "institution": "Siddhanath Campus", "country": "Nepal" },
      {
        "level": "Masters",
        "degree": "Economics",
        "institution": "Kumaun University",
        "country": "India"
      },
      {
        "level": "Masters",
        "degree": "Master of Public Policy (MPP)",
        "institution": "Meiji University",
        "country": "Japan"
      },
      {
        "level": "PhD",
        "degree": "International Politics and Diplomatic Relations",
        "institution": "Jawaharlal Nehru University",
        "country": "India"
      }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://tarajoshi.com.np/about" },
      { "platform": "Official Website", "url": "https://tarajoshi.com.np/" },
      { "platform": "Official Website", "url": "https://www.meiji.ac.jp/cip/english/graduate/governance/article02.html" }
    ]
  },
  "kp-khanal": {
    "socials": [
      { "platform": "Facebook", "url": "https://www.facebook.com/kepikhanal1/" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "Bachelor of Social Work (BSW)",
        "institution": "Texas International College",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/KP_Khanal" },
      { "platform": "Facebook", "url": "https://www.facebook.com/kepikhanal1/" }
    ]
  },
  "ashish-gajurel": {
    "socials": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/ashish-gajurel-74a03336" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "Economics & Logistics",
        "institution": "Martin-Luther-University Halle",
        "country": "Germany"
      },
      {
        "level": "Masters",
        "degree": "M.Sc. Transportation Systems; Infrastructure Design, Logistics/Supply Chain Management",
        "institution": "Technical University of Munich",
        "country": "Germany"
      }
    ],
    "sources": [
      { "platform": "LinkedIn", "url": "https://np.linkedin.com/in/ashish-gajurel-74a03336" },
      { "platform": "Other", "url": "https://scholar.google.com/citations?user=kI8M5hkAAAAJ&hl=en" }
    ]
  },
  "ranju-darshana": {
    "socials": [
      { "platform": "Website", "url": "https://ranjudarshana.com/" },
      { "platform": "Facebook", "url": "https://www.facebook.com/ranjuleads" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "Development Studies",
        "institution": "National College (Kathmandu University)",
        "country": "Nepal"
      },
      {
        "level": "Masters",
        "degree": "Political Science",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://ranjudarshana.com/about/" },
      { "platform": "Official Website", "url": "https://ranjudarshana.com/" },
      { "platform": "Facebook", "url": "https://www.facebook.com/ranjuleads" }
    ]
  }
}
'''
)


TEAM_UPDATES = json.loads(
    r'''
{
  "raj-kishor-mahato": {
    "education": [
      { "level": "SLC" },
      { "level": "+2" },
      { "level": "Bachelors", "degree": "Bachelor of Commerce" }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/raj-kishor-mahato",
        "label": "RSP - Raj Kishor Mahato candidate page"
      }
    ]
  },
  "krishna-kumar-karki": {
    "education": [
      { "level": "Bachelors", "degree": "Bachelor in Construction Management" },
      { "level": "Other", "degree": "Diploma in Sports", "country": "Japan" }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/krishna-kumar-karki",
        "label": "RSP - Krishna Kumar Karki candidate page"
      }
    ]
  },
  "pushpa-kumari-chaudhari": {
    "education": [
      { "level": "Masters", "degree": "Arts" }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/pushpa-kumari-chaudhary",
        "label": "RSP - Pushpa Kumari Chaudhary candidate page"
      }
    ]
  },
  "ujjwal-kumar-jha": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "Civil Engineering",
        "institution": "VTU",
        "country": "India"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/er-ujjwal-kumar-jha",
        "label": "RSP - Er. Ujjwal Kumar Jha candidate page"
      }
    ]
  },
  "ramakant-chaurasia": {
    "education": [
      { "level": "Other", "degree": "LSLC" }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://election.onlinekhabar.com/central-candidate/ramakant-prasad-chaurasiya",
        "label": "OnlineKhabar - Candidate Profile"
      }
    ]
  },
  "buddhi-prasad-pant": {
    "education": [
      { "level": "Bachelors", "degree": "Bachelor of Commerce" },
      { "level": "Masters", "degree": "Arts" }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/buddhi-prasad-pant",
        "label": "RSP - Buddhi Prasad Pant candidate page"
      }
    ]
  },
  "gyanendra-singh-mahata": {
    "education": [
      { "level": "SLC" },
      { "level": "Intermediate", "degree": "I.Com" },
      { "level": "Bachelors", "degree": "Bachelor of Commerce (B.Com)" },
      { "level": "Masters", "degree": "Commerce" },
      {
        "level": "Bachelors",
        "degree": "LL.B (ongoing)",
        "institution": "Nepal Open University",
        "country": "Nepal"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/gyanendra-singh-mahata",
        "label": "RSP - Gyanendra Singh Mahata candidate page"
      }
    ]
  },
  "bharat-prasad-parajuli": {
    "education": [
      {
        "level": "Bachelors",
        "degree": "Political Science",
        "institution": "Tribhuvan University"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/bharat-prasad-parajuli",
        "label": "RSP - Bharat Prasad Parajuli candidate page"
      }
    ]
  },
  "surya-bahadur-lama": {
    "education": [
      { "level": "+2" }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://election.onlinekhabar.com/central-candidate/surya-bahadur-tamang",
        "label": "OnlineKhabar - Candidate Profile"
      }
    ]
  },
  "bina-gurung": {
    "socials": [
      { "platform": "Website", "url": "https://binagurung.com/", "label": "Official website" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "degree": "Business/Commerce, General",
        "institution": "Prithivi Narayan Campus",
        "country": "Nepal"
      }
    ],
    "sources": [
      {
        "platform": "LinkedIn",
        "url": "https://np.linkedin.com/in/bina-gurung-b1a14955",
        "label": "LinkedIn profile"
      },
      {
        "platform": "Official Website",
        "url": "https://binagurung.com/",
        "label": "Official campaign website"
      }
    ]
  },
  "ganesh-karki": {
    "education": [
      {
        "level": "Masters",
        "degree": "Master of International Environmental Studies",
        "institution": "Norwegian University of Life Sciences",
        "country": "Norway"
      }
    ],
    "sources": [
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/ganess.karki/",
        "label": "Verified Facebook page"
      },
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/ganesh-karki",
        "label": "RSP candidate profile"
      }
    ]
  },
  "rajib-khatry": {
    "socials": [
      { "platform": "Website", "url": "https://rajibkhatry.com/", "label": "Official website" }
    ],
    "education": [
      {
        "level": "Bachelors",
        "institution": "Tribhuvan Vishwavidalaya",
        "country": "Nepal"
      }
    ],
    "sources": [
      {
        "platform": "LinkedIn",
        "url": "https://np.linkedin.com/in/rajib-khatry-aab23ba6",
        "label": "LinkedIn profile"
      },
      {
        "platform": "Official Website",
        "url": "https://rajibkhatry.com/",
        "label": "Official website"
      }
    ]
  },
  "prakash-pathak": {
    "education": [
      { "level": "Bachelors", "degree": "Bachelor of Business Studies (BBS)" }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/prakash-pathak",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/JournoPrakash/",
        "label": "Facebook page"
      }
    ]
  },
  "tapeshwar-yadav": {
    "education": [
      {
        "level": "Bachelors",
        "institution": "Dr. K.N. Modi University, Newai (Rajasthan)",
        "country": "India"
      }
    ],
    "sources": [
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/tapeshwar.yadav.390095/",
        "label": "Facebook page"
      }
    ]
  },
  "dharma-raj-kc": {
    "education": [
      {
        "level": "Masters",
        "degree": "Engineering",
        "institution": "Ajou University",
        "country": "South Korea"
      }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://election.ekantipur.com/profile/2285?lng=eng",
        "label": "Ekantipur - Candidate Profile"
      }
    ]
  },
  "suresh-kumar-chaudhary": {
    "education": [
      { "level": "Intermediate", "degree": "I.Com" }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://election.onlinekhabar.com/central-candidate/suresh-kumar-chaudhary",
        "label": "OnlineKhabar - Candidate Profile"
      },
      {
        "platform": "News Article",
        "url": "https://election.ekantipur.com/profile/3045?lng=eng",
        "label": "Ekantipur - Candidate Profile"
      }
    ]
  },
  "parash-mani-gelal": {
    "education": [
      {
        "level": "Masters",
        "institution": "Tribhuvan University",
        "country": "Nepal"
      }
    ],
    "sources": [
      {
        "platform": "LinkedIn",
        "url": "https://np.linkedin.com/in/parash-mani-gelal-00133b339",
        "label": "Parash Mani Gelal - LinkedIn"
      },
      {
        "platform": "News Article",
        "url": "https://election.onlinekhabar.com/central-candidate/parash-mani-gelal",
        "label": "OnlineKhabar - Candidate Profile"
      }
    ]
  },
  "asha-jha": {
    "education": [
      { "level": "Bachelors", "degree": "Public Health" }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://ekantipur.com/politics/2026/03/09/en/of-the-14-directly-elected-women-mps-13-are-from-the-rashtriya-swayamsevak-sangh-rss-03-20.html",
        "label": "Ekantipur - Women MPs feature"
      }
    ]
  },
  "sobita-gautam": {
    "socials": [
      { "platform": "Website", "url": "https://www.sobitagautam.com.np", "label": "Official website" },
      { "platform": "Twitter/X", "url": "https://twitter.com/sobita465", "label": "Sobita Gautam" },
      { "platform": "LinkedIn", "url": "https://www.linkedin.com/in/sobita-gautam", "label": "Sobita Gautam" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://www.sobitagautam.com.np", "label": "Official Website" },
      { "platform": "Twitter/X", "url": "https://twitter.com/sobita465", "label": "Embedded on official website" },
      { "platform": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Sobita_Gautam", "label": "Sobita Gautam – Wikipedia" },
      { "platform": "Other", "url": "https://www.wikidata.org/wiki/Q115406648", "label": "Sobita Gautam – Wikidata" }
    ]
  },
  "sasmit-pokharel": {
    "socials": [
      { "platform": "Website", "url": "https://sasmitpokharel.com", "label": "Official website" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://sasmitpokharel.com", "label": "Official Website" },
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/sasmit-pokharel", "label": "OnlineKhabar – Candidate Profile" }
    ]
  },
  "pukar-bam": {
    "socials": [
      { "platform": "Website", "url": "https://pukarbam.com", "label": "Official website" }
    ],
    "sources": [
      { "platform": "Official Website", "url": "https://pukarbam.com", "label": "Official Website" },
      { "platform": "News Article", "url": "https://election.onlinekhabar.com/central-candidate/pukar-bam", "label": "OnlineKhabar – Candidate Profile" }
    ]
  }
}
'''
)


FINAL_WAVE_UPDATES = json.loads(
    r'''
{
  "thakur-singh-tharu": {
    "education": [
      { "level": "Other", "degree": "Proficiency Certificate" }
    ],
    "sources": [
      {
        "platform": "Other",
        "url": "https://www.changenepal.org/election/candidate/thakur-sinha-tharu/election-2082",
        "label": "ChangeNepal 2082 candidate profile"
      },
      {
        "platform": "Other",
        "url": "https://www.changenepal.org/election/candidate/thakur-sinha-tharu/election-2079",
        "label": "ChangeNepal 2079 candidate profile"
      }
    ]
  },
  "janak-singh-dhami": {
    "education": [
      { "level": "SLC" },
      { "level": "Bachelors", "degree": "Bachelor's level study (not completed)" }
    ],
    "sources": [
      {
        "platform": "News Article",
        "url": "https://www.ratopati.com/story/549117/banana-farmer-father-now-federal-mp",
        "label": "Ratopati profile article on Janak Singh Dhami"
      },
      {
        "platform": "News Article",
        "url": "https://www.radiobelauri.org.np/news-details/1812/2026-03-08",
        "label": "Radio Belauri profile article on Janak Singh Dhami"
      }
    ]
  },
  "hari-dhakal": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/hari-dhakal",
        "label": "Official candidate page"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/hari-dhakal",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Hari_Dhakal",
        "label": "Hari Dhakal - Wikipedia"
      }
    ]
  },
  "sulav-kharel": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/sulav-kharel",
        "label": "Official candidate page"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/SulavKharelRSP/",
        "label": "Sulav Kharel Secretariat"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/sulav-kharel",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/SulavKharelRSP/",
        "label": "Sulav Kharel Secretariat"
      }
    ]
  },
  "manish-jha": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://manishjhanepal.com.np/",
        "label": "Official website"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/ManishJhaNepal1",
        "label": "Manish Jha Nepal"
      },
      {
        "platform": "Twitter/X",
        "url": "https://x.com/ManishJhaOffice",
        "label": "Manish Jha Office"
      },
      {
        "platform": "Instagram",
        "url": "https://www.instagram.com/manishjha_nepal/",
        "label": "manishjha_nepal"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://manishjhanepal.com.np/",
        "label": "Official website"
      },
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/manish-jha",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Manish_Jha_(politician)",
        "label": "Manish Jha (politician) - Wikipedia"
      }
    ]
  },
  "devaraj-pathak": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/devaraj-pathak",
        "label": "Official candidate page"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/devaraj-pathak",
        "label": "RSP candidate profile"
      }
    ]
  },
  "sagar-dhakal": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://www.sagardhakal.net/",
        "label": "Official website"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://www.sagardhakal.net/",
        "label": "Official website"
      },
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/sagar-dhakal",
        "label": "RSP candidate profile"
      }
    ]
  },
  "prakash-pathak": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/prakash-pathak",
        "label": "Official candidate page"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/JournoPrakash/",
        "label": "Prakash Pathak"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/prakash-pathak",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/JournoPrakash/",
        "label": "Prakash Pathak"
      }
    ]
  },
  "nitima-bhandari-karki": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/nitima-bhandari-karki",
        "label": "Official candidate page"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/nitima-bhandari-karki",
        "label": "RSP candidate profile"
      }
    ]
  },
  "madhukumar-chaulagain": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/madhu-kumar-chaulagai",
        "label": "Official candidate page"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/madhu.chaulagain.758/",
        "label": "Madhu Kumar Chaulagain"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/madhu-kumar-chaulagai",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/madhu.chaulagain.758/",
        "label": "Madhu Kumar Chaulagain"
      }
    ]
  },
  "dhannjaya-regmi": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://drdhananjayregmi.com/",
        "label": "Official website"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/profile.php?id=61584494383942",
        "label": "Dr Dhananjay Regmi"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://drdhananjayregmi.com/",
        "label": "Official website"
      },
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/dr-dhananjaya-regmi",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/profile.php?id=61584494383942",
        "label": "Dr Dhananjay Regmi"
      }
    ]
  },
  "ashok-kumar-chaudhary": {
    "socials": [
      {
        "platform": "Website",
        "url": "https://rspnepal.org/election-2082/ashok-kumar-chaudhary",
        "label": "Official candidate page"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/ashokkumar.chaudhary1/",
        "label": "Ashok Kumar Chaudhary"
      },
      {
        "platform": "Instagram",
        "url": "https://www.instagram.com/ashokkumar.chaudhary1",
        "label": "ashokkumar.chaudhary1"
      }
    ],
    "sources": [
      {
        "platform": "Official Website",
        "url": "https://rspnepal.org/election-2082/ashok-kumar-chaudhary",
        "label": "RSP candidate profile"
      },
      {
        "platform": "Facebook",
        "url": "https://www.facebook.com/ashokkumar.chaudhary1/",
        "label": "Ashok Kumar Chaudhary"
      },
      {
        "platform": "Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Ashok_Kumar_Chaudhary",
        "label": "Ashok Kumar Chaudhary - Wikipedia"
      }
    ]
  }
}
'''
)


MANUAL_SOCIALS = {
    "balendra-shah": [
        {"platform": "Facebook", "url": "https://www.facebook.com/balenOfficial/"},
        {"platform": "Instagram", "url": "https://www.instagram.com/balenshah/"},
    ],
    "rabi-lamichhane": [
        {"platform": "Facebook", "url": "https://www.facebook.com/rabi.nikitalamichhane/"}
    ],
}


SOCIAL_PREFERENCES = {
    "jagdish-kharel": {
        "Facebook": "https://www.facebook.com/Jagdishkharelofficial/",
    },
    "tara-prasad-joshi": {
        "Facebook": "https://www.facebook.com/profile.php?id=100086656631042",
    },
}


LEVEL_ORDER = {
    "SLC": 0,
    "Intermediate": 1,
    "+2": 2,
    "Bachelors": 3,
    "Masters": 4,
    "PhD": 5,
    "Other": 6,
}


def norm(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def normalize_url(url):
    url = url.strip()
    url = url.replace("http://www.twitter.com/", "https://twitter.com/")
    url = url.replace("http://twitter.com/", "https://twitter.com/")
    url = url.replace("http://www.facebook.com/", "https://www.facebook.com/")
    if url.endswith("/") and "profile.php?" not in url:
        url = url.rstrip("/")
    return url


def normalize_social_url(platform, url):
    url = normalize_url(url)
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    segments = [segment for segment in parsed.path.split("/") if segment]

    if platform == "Website":
        return url

    if platform == "Twitter/X":
        if not segments or segments[0].lower() in {"share", "intent", "hashtag", "search", "i", "home", "explore"}:
            return None
        return f"https://twitter.com/{segments[0]}"

    if platform == "Instagram":
        if not segments or segments[0].lower() in {"p", "reel", "reels", "stories", "explore", "accounts"}:
            return None
        return f"https://www.instagram.com/{segments[0]}"

    if platform == "LinkedIn":
        if len(segments) >= 2 and segments[0].lower() == "in":
            return f"https://www.linkedin.com/in/{segments[1]}"
        return None

    if platform == "Facebook":
        if parsed.path == "/profile.php":
            profile_id = parse_qs(parsed.query).get("id", [None])[0]
            return f"https://www.facebook.com/profile.php?id={profile_id}" if profile_id else None
        if segments and segments[0].lower() == "people" and len(segments) >= 3:
            return f"https://www.facebook.com/people/{segments[1]}/{segments[2]}"
        if segments and segments[0].lower() == "p" and len(segments) >= 2:
            return f"https://www.facebook.com/p/{segments[1]}"
        if not segments or segments[0].lower() in {"share", "hashtag", "sharer.php", "dialog", "login", "events", "groups", "photo.php"}:
            return None
        return f"https://www.facebook.com/{segments[0]}"

    return url


def social_label(platform, candidate_name):
    return "Official website" if platform == "Website" else candidate_name


def source_label(source):
    platform = source.get("platform")
    url = source.get("url", "")
    if platform == "Wikipedia":
        return "Wikipedia"
    if platform == "Official Website":
        return "Official Website"
    if platform == "Facebook":
        return "Facebook"
    if platform == "LinkedIn":
        return "LinkedIn"
    if platform == "Twitter/X":
        return "Twitter / X"
    if "election.onlinekhabar.com" in url:
        return "OnlineKhabar – Candidate Profile"
    if "election.ekantipur.com" in url:
        return "Ekantipur – Candidate Profile"
    return source.get("label")


def dedupe_socials(items):
    out = []
    seen = set()
    for item in items:
        if not item or not item.get("url"):
            continue
        url = normalize_social_url(item["platform"], item["url"])
        if not url:
            continue
        key = (item["platform"], url)
        if key in seen:
            continue
        seen.add(key)
        entry = {"platform": item["platform"], "url": url}
        if item.get("label"):
            entry["label"] = item["label"]
        out.append(entry)
    return out


def apply_social_preferences(candidate_id, socials):
    prefs = SOCIAL_PREFERENCES.get(candidate_id)
    if not prefs:
        return socials

    filtered = []
    for social in socials:
        preferred_url = prefs.get(social["platform"])
        if preferred_url and normalize_social_url(social["platform"], social["url"]) != normalize_social_url(social["platform"], preferred_url):
            continue
        filtered.append(social)
    return filtered


def dedupe_sources(items):
    out = []
    seen = set()
    for item in items:
        if not item or not item.get("url"):
            continue
        url = normalize_url(item["url"])
        key = (item["platform"], url)
        if key in seen:
            continue
        seen.add(key)
        entry = {"platform": item["platform"], "url": url}
        label = item.get("label") or source_label(item)
        if label:
            entry["label"] = label
        out.append(entry)
    return out


def add_education_entry(entries, level, degree=None, institution=None, country=None):
    entry = {"level": level}
    if degree:
        entry["degree"] = degree.strip()
    if institution:
        entry["institution"] = institution.strip()
    if country:
        entry["country"] = country.strip()
    entries.append(entry)


def parse_ekantipur_education(raw, has_existing=False):
    if not raw:
        return []

    text = re.sub(r"\s+", " ", raw).strip()
    lower = text.lower()
    entries = []

    if text in {"कानुन व्यवसायी", "इन्जिनियर", "सिभिल ईन्जीनियर", "दश"}:
        return []
    if has_existing and text in {"BTU"}:
        return []

    if len(text) > 80:
        if "एसएलसी" in text or "SLC" in text.upper():
            add_education_entry(entries, "SLC")
        if any(token in text for token in ["आईए", "I.A", "I.Sc", "प्रमाणपत्र"]):
            add_education_entry(entries, "Intermediate")
        if "MBBS" in text.upper() or "एमबीबीएस" in text:
            add_education_entry(entries, "Bachelors", "MBBS")
        if "स्नातक" in text or "Bachelor" in text:
            add_education_entry(entries, "Bachelors")
        if "General Surgery" in text or "जनरल सर्जरी" in text:
            add_education_entry(entries, "Masters", "General Surgery")
        elif any(token in text for token in ["स्नातकोत्तर", "Masters", "Master", "MBA", "MSc", "एम.ए", "एम ए"]):
            add_education_entry(entries, "Masters")
        if "विद्यावारिधि" in text or "PhD" in text or "PHD" in text.upper():
            add_education_entry(entries, "PhD", "PhD (ongoing)" if "अध्ययनरत" in text else None)
        return entries

    if text in {"+2", "10+2", "१०+२ पास"}:
        return [{"level": "+2"}]
    if text in {"SLC", "एस एल सीढ"}:
        return [{"level": "SLC"}]
    if text in {
        "आइ ए",
        "आइए",
        "आई कम",
        "I.Sc.",
        "Intermediate in commerce",
        "PCL(+2)",
        "प्रमाणपत्र तह",
        "प्रविणता प्रमाणपत्र तह",
        "प्रवीणता प्रमाणपत्र तह",
        "प्रविणता प्रमाण पत्र political science",
    }:
        degree_map = {
            "Intermediate in commerce": "Commerce",
            "I.Sc.": "Science",
            "आई कम": "Commerce",
            "आइ ए": "IA",
            "आइए": "IA",
            "PCL(+2)": "PCL",
            "प्रविणता प्रमाण पत्र political science": "Political Science",
        }
        degree = degree_map.get(text)
        return [{"level": "Intermediate", **({"degree": degree} if degree else {})}]

    if text in {
        "BL",
        "Bachelor",
        "स्नातक",
        "स्नातक तह",
        "स्तानतक",
        "स्तानतक मेकानिकल इन्जिनियरिङ्ग",
        "स्तानक मेकानिकल इन्जिनियरिङ्ग",
        "स्नातक रनिङ",
        "स्नातक (सोइल कन्जर्भेशन)",
        "वि.एस.सी.",
        "विए पास",
        "बीएड",
        "Bcahelor Of Medicine",
        "जलस्रोत ईन्जिनियरिङमा डिग्री",
        "Anthropology, Political Science",
        "ब्यवस्थापन संकायमा डिग्रि सम्मको अध्ययन पुरा गरेका छन्",
        "कानुनका विद्यार्थी",
    }:
        degree_map = {
            "BL": "BL",
            "स्तानतक मेकानिकल इन्जिनियरिङ्ग": "Mechanical Engineering",
            "स्तानक मेकानिकल इन्जिनियरिङ्ग": "Mechanical Engineering",
            "स्नातक रनिङ": "Bachelor studies (ongoing)",
            "स्नातक (सोइल कन्जर्भेशन)": "Soil Conservation",
            "वि.एस.सी.": "BSc",
            "विए पास": "BA",
            "बीएड": "BEd",
            "Bcahelor Of Medicine": "Bachelor of Medicine",
            "जलस्रोत ईन्जिनियरिङमा डिग्री": "Water Resources Engineering",
            "Anthropology, Political Science": "Anthropology, Political Science",
            "ब्यवस्थापन संकायमा डिग्रि सम्मको अध्ययन पुरा गरेका छन्": "Management",
            "कानुनका विद्यार्थी": "Law (ongoing)",
        }
        degree = degree_map.get(text)
        return [{"level": "Bachelors", **({"degree": degree} if degree else {})}]

    if text in {
        "MA",
        "MSC",
        "MBA",
        "Masters",
        "एम. ए.",
        "एम. ए",
        "एम.ए.",
        "एम ए राजनीति शास्त्र",
        "एम.ए. (राजनितिशास्त्र)",
        "एम.बि.ए",
        "Master in political Science",
        "अंग्रेजी साहित्यमा स्नातक, एमबिए",
        "मास्टर डिग्री : Transportation Systems",
        "स्नातकोत्तर",
        "स्नातकोत्तर (कानून)",
        "स्नातकोउत्तर",
        "स्नाकोत्तर",
        "स्नात्तकोतर",
        "स्नात्तकोत्तर",
        "स्नोकोत्तर",
        "दक्षिण कोरियाको अजु विश्वविद्यालय (Ajou University) बाट इन्जिनियरिङमा स्नातकोत्तर",
    }:
        degree_map = {
            "MA": "MA",
            "MSC": "MSc",
            "MBA": "MBA",
            "एम. ए.": "MA",
            "एम. ए": "MA",
            "एम.ए.": "MA",
            "एम ए राजनीति शास्त्र": "Political Science",
            "एम.ए. (राजनितिशास्त्र)": "Political Science",
            "एम.बि.ए": "MBA",
            "Master in political Science": "Political Science",
            "अंग्रेजी साहित्यमा स्नातक, एमबिए": "MBA",
            "मास्टर डिग्री : Transportation Systems": "Transportation Systems",
            "स्नातकोत्तर (कानून)": "Law",
            "दक्षिण कोरियाको अजु विश्वविद्यालय (Ajou University) बाट इन्जिनियरिङमा स्नातकोत्तर": "Engineering",
        }
        degree = degree_map.get(text)
        institution = "Ajou University" if "Ajou University" in text else None
        country = "South Korea" if "Ajou University" in text else None
        return [
            {
                "level": "Masters",
                **({"degree": degree} if degree else {}),
                **({"institution": institution} if institution else {}),
                **({"country": country} if country else {}),
            }
        ]

    if any(token in lower for token in ["phd", "p.hd"]) or any(token in text for token in ["विद्यावारिधि", "विद्यावारिधी", "बिध्यावारिधी", "पीएचडी"]):
        degree = None
        if "economics" in lower or "अर्थशास्त्र" in text:
            degree = "Economics"
        elif "अध्ययनरत" in text:
            degree = "PhD (ongoing)"
        return [{"level": "PhD", **({"degree": degree} if degree else {})}]

    if text in {"D.M.", "डिप्लोमा इन सिभिल इन्जिनियरिङ्ग", "नर्सिङ", "Ied"}:
        degree_map = {
            "D.M.": "D.M.",
            "डिप्लोमा इन सिभिल इन्जिनियरिङ्ग": "Diploma in Civil Engineering",
            "नर्सिङ": "Nursing",
            "Ied": "I.Ed.",
        }
        return [{"level": "Other", "degree": degree_map[text]}]

    if "स्नातकोत्तर" in text or "master" in lower or "mba" in lower or "msc" in lower or "m.a" in lower:
        return [{"level": "Masters"}]
    if "स्नातक" in text or "bachelor" in lower or "engineer" in lower or lower == "bl":
        return [{"level": "Bachelors"}]
    if "प्रमाणपत्र" in text or "intermediate" in lower:
        return [{"level": "Intermediate"}]
    if "slc" in lower or "एसएलसी" in text:
        return [{"level": "SLC"}]
    return []


def merge_education(existing, extra):
    merged = []
    for item in (existing or []) + (extra or []):
        if not item or not item.get("level"):
            continue
        merged.append({k: v for k, v in item.items() if v not in (None, "", [])})

    out = []
    for item in merged:
        duplicate = False
        for other in merged:
            if item is other:
                continue
            if item.get("level") != other.get("level"):
                continue
            if not item.get("degree") and not item.get("institution") and not item.get("country"):
                if other.get("degree") or other.get("institution") or other.get("country"):
                    duplicate = True
                    break
        if not duplicate:
            out.append(item)

    deduped = []
    seen = set()
    for item in out:
        key = (
            item.get("level"),
            (item.get("degree") or "").lower(),
            (item.get("institution") or "").lower(),
            (item.get("country") or "").lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    deduped.sort(key=lambda e: (LEVEL_ORDER.get(e["level"], 99), e.get("degree", ""), e.get("institution", "")))
    return deduped


def website_social_platform(url):
    if "facebook.com" in url:
        return "Facebook"
    if "instagram.com" in url:
        return "Instagram"
    if "linkedin.com" in url:
        return "LinkedIn"
    if "twitter.com" in url or "x.com" in url:
        return "Twitter/X"
    return None


def extract_socials_from_website(url, candidate_name):
    host = urlparse(url).netloc.lower()
    if "rspnepal.org" in host:
        return []

    try:
        html = requests.get(url, timeout=20, headers=REQ_HEADERS).text
    except Exception:
        return []

    soup = BeautifulSoup(html, "html.parser")
    socials = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if any(
            bad in href
            for bad in [
                "sharer.php",
                "intent/tweet",
                "/share?",
                "share?u=",
                "facebook.com/robusteducationcenter",
            ]
        ):
            continue

        platform = website_social_platform(href)
        if not platform:
            continue

        socials.append(
            {
                "platform": platform,
                "url": href,
                "label": social_label(platform, candidate_name),
            }
        )

    return dedupe_socials(socials)


def extract_vote_rows(soup):
    rows = {}
    for table in soup.select("table.table.table-bordered"):
        headers = [th.get_text(" ", strip=True) for th in table.select("thead th")]
        if headers[:3] != ["Candidate", "Party", "Total Votes"]:
            continue

        for tr in table.select("tbody tr"):
            candidate_link = tr.select_one("a.candidate-name-link")
            vote_node = tr.select_one(".votecount p")
            if not candidate_link or not vote_node:
                continue

            href = candidate_link.get("href")
            name = " ".join(candidate_link.stripped_strings).strip()
            vote_text = vote_node.get_text(" ", strip=True).replace(",", "")
            if not vote_text.isdigit():
                continue

            votes = int(vote_text)
            key = href or name
            if key not in rows or votes > rows[key]["votes"]:
                rows[key] = {
                    "href": href,
                    "name": name,
                    "votes": votes,
                }

    return list(rows.values())


def fetch_ekantipur_mapping(candidates):
    home = requests.get("https://election.ekantipur.com/?lng=eng", timeout=30, headers=REQ_HEADERS).text
    slug_to_name = {}
    for slug, name in re.findall(r"dists\['([^']+)'\]\s*=\s*\{\"name\":\"([^\"]+)\"", home):
        slug_to_name[slug] = name

    name_to_slug = {norm(name): slug for slug, name in slug_to_name.items()}
    district_aliases = {
        "kavrepalanchok": "kavrepalanchowk",
        "dhanusha": "dhanusa",
        "nawalpur": "nawalparasieast",
        "nawalparasieast": "nawalparasieast",
        "nawalparasiwest": "nawalparasiwest",
        "nawalparasi": "nawalparasiwest",
        "sindhupalchok": "sindhupalchowk",
        "rautahat": "rauthat",
        "dolakha": "dolkha",
    }

    def district_slug(name):
        key = norm(name)
        return district_aliases.get(key) or name_to_slug.get(key)

    def fetch(candidate):
        seat = candidate["constituency"]["name"].split("-")[-1]
        province = candidate["constituency"]["provinceNumber"]
        dslug = district_slug(candidate["constituency"]["district"])
        if not dslug:
            return candidate["id"], None

        url = f"https://election.ekantipur.com/pradesh-{province}/district-{dslug}/constituency-{seat}?lng=eng"
        try:
            html = requests.get(url, timeout=20, headers=REQ_HEADERS).text
        except Exception:
            return candidate["id"], None

        soup = BeautifulSoup(html, "html.parser")
        vote_rows = extract_vote_rows(soup)
        target = norm(candidate["name"])
        links = []
        for a in soup.select('a[href*="/profile/"]'):
            name = " ".join(a.stripped_strings).strip()
            href = a.get("href")
            if name and href and "/profile/" in href:
                score = SequenceMatcher(None, target, norm(name)).ratio()
                links.append((name, href, score))

        if candidate["id"] == "ranju-darshana":
            filtered = [item for item in links if "ranju" in item[0].lower()]
            best = max(filtered, key=lambda x: x[2]) if filtered else (max(links, key=lambda x: x[2]) if links else None)
        else:
            best = max(links, key=lambda x: x[2]) if links else None

        if not best:
            return candidate["id"], None
        if candidate["id"] != "ranju-darshana" and best[2] < 0.70:
            return candidate["id"], None

        purl = "https://election.ekantipur.com" + best[1]
        education_text = None
        try:
            phtml = requests.get(purl, timeout=20, headers=REQ_HEADERS).text
            psoup = BeautifulSoup(phtml, "html.parser")
            for tr in psoup.select("table tr"):
                cells = tr.find_all("td")
                if len(cells) >= 2 and cells[0].get_text(" ", strip=True) == "Education":
                    education_text = cells[1].get_text(" ", strip=True)
                    break
        except Exception:
            pass

        winner_votes = None
        for row in vote_rows:
            if row.get("href") == best[1]:
                winner_votes = row["votes"]
                break

        if winner_votes is None and vote_rows:
            by_name = max(
                vote_rows,
                key=lambda row: SequenceMatcher(None, target, norm(row["name"])).ratio(),
            )
            if SequenceMatcher(None, target, norm(by_name["name"])).ratio() >= 0.70:
                winner_votes = by_name["votes"]

        total_valid_votes = sum(row["votes"] for row in vote_rows) if vote_rows else None

        return candidate["id"], {
            "profile_url": purl,
            "education_text": education_text,
            "constituency_url": url,
            "constituency_vote": winner_votes,
            "total_valid_votes": total_valid_votes,
        }

    results = {}
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(fetch, candidate): candidate["id"] for candidate in candidates}
        for future in as_completed(futures):
            cid, data = future.result()
            if data:
                results[cid] = data
    return results


def main():
    candidates = json.loads(DATA_PATH.read_text())
    ek_updates = fetch_ekantipur_mapping(candidates)
    social_sweep_updates = (
        json.loads(SOCIAL_SWEEP_PATH.read_text()) if SOCIAL_SWEEP_PATH.exists() else {}
    )

    for candidate in candidates:
        cid = candidate["id"]
        candidate_name = candidate["name"]
        update_blocks = [
            RESEARCH_UPDATES.get(cid, {}),
            TEAM_UPDATES.get(cid, {}),
            FINAL_WAVE_UPDATES.get(cid, {}),
            social_sweep_updates.get(cid, {}),
        ]

        candidate_sources = list(candidate.get("sources", []))
        candidate_socials = list(candidate.get("socials", []))
        extra_education = []

        for update in update_blocks:
            candidate_socials.extend(update.get("socials", []))
            candidate_sources.extend(update.get("sources", []))
            extra_education.extend(update.get("education", []))

        for social in MANUAL_SOCIALS.get(cid, []):
            social = {
                **social,
                "label": social_label(social["platform"], candidate_name),
            }
            candidate_socials.append(social)

        ek = ek_updates.get(cid)
        parsed_ek_education = []
        if ek:
            candidate_sources.append(
                {
                    "platform": "News Article",
                    "url": ek["profile_url"],
                    "label": "Ekantipur – Candidate Profile",
                }
            )
            if ek.get("constituency_url"):
                candidate_sources.append(
                    {
                        "platform": "News Article",
                        "url": ek["constituency_url"],
                        "label": "Ekantipur – Constituency Result",
                    }
                )
            parsed_ek_education = parse_ekantipur_education(
                ek.get("education_text") or "",
                has_existing=bool(candidate.get("education")),
            )

        candidate["education"] = merge_education(
            candidate.get("education", []),
            extra_education + parsed_ek_education,
        )
        if ek and ek.get("constituency_vote") is not None:
            candidate["votesReceived"] = ek["constituency_vote"]
        if ek and ek.get("total_valid_votes") is not None:
            candidate["totalValidVotes"] = ek["total_valid_votes"]
            if candidate.get("votesReceived") is not None and candidate["totalValidVotes"] > 0:
                candidate["voteSharePercent"] = round(
                    candidate["votesReceived"] / candidate["totalValidVotes"] * 100,
                    2,
                )
            if candidate.get("winMargin") is not None and candidate["totalValidVotes"] > 0:
                candidate["winMarginPercent"] = round(
                    candidate["winMargin"] / candidate["totalValidVotes"] * 100,
                    2,
                )

        website_socials = []
        for social in candidate_socials:
            if social.get("platform") == "Website":
                website_socials.extend(
                    extract_socials_from_website(social["url"], candidate_name)
                )
        candidate_socials.extend(website_socials)

        cleaned_socials = dedupe_socials(
            [
                {
                    **social,
                    "label": social.get("label")
                    or social_label(social["platform"], candidate_name),
                }
                for social in candidate_socials
            ]
        )
        cleaned_socials = apply_social_preferences(cid, cleaned_socials)
        if cleaned_socials:
            candidate["socials"] = cleaned_socials
        else:
            candidate.pop("socials", None)

        candidate["sources"] = dedupe_sources(candidate_sources)
        candidate["lastUpdated"] = LAST_UPDATED

    DATA_PATH.write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n")

    print("updated_candidates", len(candidates))
    print("candidates_with_socials", sum(1 for c in candidates if c.get("socials")))
    print("missing_education", sum(1 for c in candidates if not c.get("education")))


if __name__ == "__main__":
    main()
