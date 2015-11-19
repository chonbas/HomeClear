from . import db, Listing, Tax, Image, School, Crime
import hashlib

taxRates =   [5.1, 6.2, 7.8, 9.8, 4.8, 3.4, 7.1, 5.0, 9.1, 3.8]

crimeRates = [1.2, 3.5, 4.6, 9.5, 10.5, 19.8, 7.6, 5.0, 4.2, 31.3]

elementarySchools = [Eastside Institute, Greenfield Academy, South Fork Academy,
                    Faith Elementary, Seal Gulch School, Diamond Middle School,
                    Riverview Middle School, Fortuna Academy, Sierra Grammar School,
                    Seaside Elementary]

highSchools = [Ravenwood High School,Vista High School,Mammoth High,White Mountain High,
                Seacoast High,Edgewood High,Silverleaf High School,Winterville High School,
                Mountainridge High,Bayshore High]

universities = [Storm Coast College, Tranquillity Technical School,
                Vista University, Grand Ridge Institute, Meadows University,
                Central Valley College, Palm Valley University, Sunnyside College,
                Big Pine University, Forest Lake University]


def generateListing(string):

    listing = Listing(address=string,
            username=form.username.data,
            password=form.password.data)
    db.session.add(user)
    db.session.commit()
