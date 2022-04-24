import sys
sys.path.insert(1, '../')



from flask import session

from db_models.plugins import get_one_plugin, get_one_plugin_crud, init_plugins, set_plugin_token
from config import init_config
from tools.db_tool import init_db, init_tables
from unittest.mock import patch
from unittest.mock import Mock
import tools.db_tool
from alchemy_mock.mocking import AlchemyMagicMock

import sqlalchemy as db

from db_models.users import UserModel, add_user, check_one_user, get_by_username
import unittest

session = None
engine = None
names =  [
"Aaberg","Aalst","Aara","Aaren","Aarika","Aaron","Aaronson","Ab","Aba","Abad","Abagael","Abagail","Abana","Abate","Abba","Abbate"
,
"Abbe","Abbey","Abbi","Abbie","Abbot","Abbotsen","Abbotson","Abbotsun","Abbott","Abbottson","Abby","Abbye","Abdel","Abdella","Abdu"
,
"Abdul","Abdulla","Abe","Abebi","Abel","Abelard","Abell","Abercromby","Abernathy","Abernon","Abert","Abeu","Abey","Abie","Abigael"
,
"Abigail","Abigale","Abijah","Abisha","Abisia","Abixah","Abner","Aborn","Abott","Abra","Abraham","Abrahams","Abrahamsen","Abrahan"
,
"Abram","Abramo","Abrams","Abramson","Abran","Abroms","Absa","Absalom","Abshier","Acacia","Acalia","Accalia","Ace","Acey","Acherman"
,
"Achilles","Achorn","Acie","Acima","Acker","Ackerley","Ackerman","Ackler","Ackley","Acquah","Acus","Ad","Ada","Adabel","Adabelle"
,
"Adachi","Adah","Adaha","Adai","Adaiha","Adair","Adal","Adala","Adalai","Adalard","Adalbert","Adalheid","Adali","Adalia","Adaliah"
,
"Adalie","Adaline","Adall","Adallard","Adam","Adama","Adamec","Adamek","Adamik","Adamina","Adaminah","Adamis","Adamo","Adamok"
,
"Adams","Adamsen","Adamski","Adamson","Adamsun","Adan","Adao","Adar","Adara","Adaurd","Aday","Adda","Addam","Addi","Addia"]
        ###################################################
passwords = [
  "aaa",  "aarp",  "abb",  "abbott",  "abbvie",  "abogado",  "abudhabi",  "ac",  "academy",  "accenture",  "accountant",  "accountants",
  "aco",  "active",  "actor",  "ad",  "adac",  "ads",  "adult",  "ae",  "aeg",  "aero",  "af",  "afl",  "ag",  "agency",  "ai",  "aig",
  "airforce",  "airtel",  "al",  "alibaba",  "alipay",  "allfinanz",  "ally",  "alsace",  "am",  "amica",  "amsterdam",  "analytics",
  "android",  "anquan",  "ao",  "apartments",  "app",  "apple",  "aq",  "aquarelle",  "ar",  "aramco",  "archi",  "army",  "arpa",
  "arte",  "as",  "asia",  "associates",  "at",  "attorney",  "au",  "auction",  "audi",  "audio",  "author",  "auto",  "autos",
  "avianca",  "aw",  "aws",  "ax",  "axa",  "az",  "azure",  "ba",  "baby",  "baidu",  "band",  "bank",  "bar",  "barcelona",
  "barclaycard",  "barclays",  "barefoot",  "bargains",  "bauhaus",  "bayern",  "bb",  "bbc",  "bbva",  "bcg",  "bcn",  "bd",  "be",
  "beats",  "beer",  "bentley",  "berlin",  "best",  "bet",  "bf",  "bg",  "bh",  "bharti",  "bi",  "bible",  "bid",  "bike",  "bing",
  "bingo",  "bio",  "biz",  "bj",  "black",  "blackfriday",  "bloomberg",  "blue",  "bm",  "bms",  "bmw",  "bn",  "bnl",  "bnpparibas",
  "bo",  "boats",  "boehringer",  "bom"]
        ####################################################
emails = [
"edeevey0@yandex.ru", "krichie1@bizjournals.com", "wdansken2@fc2.com", "ovandenvelden3@jiathis.com", "rcutridge4@spotify.com", 
"dledamun5@sciencedaily.com", "rpercy6@unblog.fr", "hwhife7@cocolog-nifty.com", "ksnaddin8@ycombinator.com", "mmcart9@army.mil", 
"kdurdya@pcworld.com", "khacksbyb@bandcamp.com", "huwinsc@nhs.uk", "hcrippend@gizmodo.com", "hghioe@princeton.edu", 
"adommersenf@miitbeian.gov.cn", "ptideyg@hhs.gov", "btuleyh@opera.com", "bablei@fda.gov", "tsnooksj@edublogs.org", 
"epeperellk@vimeo.com", "ebutlerl@admin.ch", "regglesonm@latimes.com", "nledekkern@google.ru", "hbloyeso@topsy.com", 
"imacelholmp@msn.com", "ewhittakerq@bravesites.com", "kitzhakr@amazon.com", "gcowans@surveymonkey.com", "istanfieldt@washington.edu", 
"baspinellu@nih.gov", "dmazzeov@mozilla.org", "pmartinew@quantcast.com", "nmarttx@unesco.org", "tguinnessy@csmonitor.com", 
"tbroomheadz@forbes.com", "mwalstow10@washingtonpost.com", "tgeillier11@globo.com", "abriat12@usatoday.com", 
"odunmore13@stumbleupon.com", "ssaltsberger14@linkedin.com", "wmorffew15@acquirethisname.com", "handreutti16@cornell.edu", 
"sstanes17@tinyurl.com", "cbywaters18@theguardian.com", "gharlock19@timesonline.co.uk", "ihawkridge1a@shutterfly.com", 
"mkruschov1b@indiatimes.com", "cmorin1c@columbia.edu", "mgoodbarr1d@sun.com", "ichiverton1e@nydailynews.com", 
"aantoszewski1f@mapy.cz", "ikun1g@buzzfeed.com", "scowpland1h@techcrunch.com", "lclemoes1i@dell.com", "ccraney1j@weebly.com", 
"ogregoratti1k@foxnews.com", "kwhapples1l@squidoo.com", "ejewson1m@myspace.com", "jborthram1n@oracle.com", "esute1o@forbes.com", 
"mbernth1p@spiegel.de", "jkenewell1q@smh.com.au", "rblackster1r@si.edu", "ytossell1s@virginia.edu", "dallbones1t@lulu.com", 
"achatres1u@com.com", "vmcdell1v@blogs.com", "aodgers1w@fastcompany.com", "ewestwell1x@vk.com", "elangworthy1y@abc.net.au", 
"fharty1z@cornell.edu", "ekniveton20@usgs.gov", "rskeemor21@vk.com", "bbrightwell22@europa.eu", "ldelafeld23@archive.org", 
"ekubasiewicz24@cnet.com", "berdes25@narod.ru", "jfaers26@weebly.com", "kaldiss27@wikia.com", "dforsdicke28@usnews.com", 
"rrewbottom29@edublogs.org", "ostribling2a@symantec.com", "agomm2b@mac.com", "cnajara2c@phoca.cz", "lbeefon2d@qq.com", 
"fdorkens2e@house.gov", "fnockalls2f@webeden.co.uk", "cschubert2g@bloglovin.com", "blawille2h@geocities.com", 
"atennock2i@utexas.edu", "mwigley2j@wikimedia.org", "dradley2k@shinystat.com", "eredford2l@narod.ru", "lsabie2m@smugmug.com", 
"brobelin2n@miibeian.gov.cn", "cberni2o@cbslocal.com", "nblas2p@digg.com", "ckrimmer2q@scientificamerican.com", 
"awhiscard2r@cdc.gov"]
########################################
class TestApp(unittest.TestCase):
    global session
    global names 
    global emails 
    global passwords 

    def test4_set_plugin(self):
        plugin_lists = [
            {
                'p_name':'whois',
                'params':'token',
                'link':'whoisxmlapi.com',
                'description':'',
                'image':'pluginp/whois.png'
            },   
            {
                'p_name':'github',
                'params':'',
                'link':'https://api.github.com/users/',
                'description':'',
                'image':'pluginp/github.png'
            },
            {
                'p_name':'instagram',
                'params':'',
                'link':'https://instagram.com/',
                'description':'',
                'image':'pluginp/instagram.png'
            },
            {
                'p_name':'telegram',
                'params':'',
                'link':'https://t.me/',
                'description':'',
                'image':'pluginp/telegram.png'
            }
            ]
        for p_name in plugin_lists:     
            plugin = get_one_plugin(p_name['p_name'] , -1 , engine)
            user = get_by_username(names[0] ,engine)
            set_plugin_token(plugin , user ,engine , 'test' , 'test2' , 'test3' )
        
        
    def test3_init_plugin(self):
        init_plugins(engine)
        
    def test2_login(self):
        for pointer in range(len(emails)):
            name = names[pointer]
            password = passwords[pointer]
            self.assertIsNotNone(check_one_user(name , password , engine))
    def test1_register(self ):
        for pointer in range(len(emails)):
            name = names[pointer]
            email = emails[pointer]
            password = passwords[pointer]
            self.assertEqual(True, add_user(name, email, password, engine ))


if __name__ == "__main__":
    engine = db.create_engine('sqlite:///:memory:')
    init_tables(engine)

    unittest.main()