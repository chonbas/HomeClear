from . import db
from .models import Listing, Tax, Image, School, Crime, Geo
import hashlib, locale

taxRates =   [5.1, 6.2, 7.8, 9.8, 4.8, 3.4, 7.1, 5.0, 9.1, 3.8]

crimeRates = [1.2, 3.5, 4.6, 9.5, 10.5, 19.8, 7.6, 5.0, 4.2, 31.3]

elementarySchools = ['Eastside Institute', 'Greenfield Academy', 'South Fork Academy',
                    'Faith Elementary', 'Seal Gulch School', 'Diamond Middle School',
                    'Riverview Middle School', 'Fortuna Academy', 'Sierra Grammar School',
                    'Seaside Elementary']

highSchools = ['Ravenwood High School','Vista High School', 'Mammoth High', 'White Mountain High',
                'Seacoast High', 'Edgewood High', 'Silverleaf High School', 'Winterville High School',
                'Mountainridge High', 'Bayshore High']

universities = ['Storm Coast College', 'Tranquillity Technical School',
                'Vista University', 'Grand Ridge Institute', 'Meadows University',
                'Central Valley College', 'Palm Valley University', 'Sunnyside College',
                'Big Pine University', 'Forest Lake University']

realtors = ['Yahaira Townson','Yang Uriarte','Caron Carbaugh','Annabelle Silk',
            'Harry Skeeter','Osvaldo Shull','Alec Foucher','Pei Peed', 'Marketta Lippard',
            'Blanch Sim']

dates=['5/25/2000','12/4/2000','4/18/2002','6/27/2005', '1/22/2007','2/11/2010','10/2/2011',
        '5/18/2013', '2/16/2014', '1/15/2015']

moreReading = ['Wildlife: http://www.sfbaywildlife.info/species/species.htm',
            'Earthquakes: http://www.earthquakesafety.com/earthquake-faults.html',
            'Sex Offender Registry: https://www.fbi.gov/scams-safety/registry',
            'Tornado: http://www.spc.noaa.gov/faq/tornado/safety.html',
            'Hurricane: http://www.americanchemistry.com/Hurricane-Safety?gclid=CIf30IncmMkCFYZbfgodh5gLMA',
            'Zoning: http://www.sf-planning.org/index.aspx?page=2205']

crimes = ['Motor vehicle theft','Domestic violence report','Aggravated assault',
            'Burglary','Armed Robbery','Public Indecency','Speeding',
            'Public Urination','Drugs: Possession', 'Drugs: Distribution','Driving under the influence',
            'Loitering','Murder', 'Reckless Driving']

geo_incidents = ['Earthquake', 'Flooding', 'Tornado', 'Hurricane','Wildfire']

sellers =['Lacy Woolard','Rhea Rodenberg','Belia Mattis','Roxy Antonio','Kaye Favero',
        'Wen Dineen','Darrel Lachapelle','Jon Lentini','Amos Tulley','Essie Stejskal',
        'Criselda Nations','Chadwick Grear','Lashon Coletti','Marisa Haugland','Marcel Band',
        'Juliette Gathers','Melida Lundell','August Spriggs','Cleotilde Cropp','Nelly Taft',
        'Yvonne Cadena','Teri Arguelles','Neta Larrimore','Virgie Thoms','Tammy Molinar',
        'Melynda Bickett']

schoolDistricts =['Union School District', 'Heights School District', 'Bear River School District',
                'Providence School District', 'River Heights School District', 'Cottonwood School District',
                'Serra School District', 'Alto School District', 'Redwood School District',
                'City Heights School District', 'Foothills School District', 'Morgan School District']


def getHash(s):
    hasher = hashlib.md5()
    hasher.update(s)
    f= float(int(hasher.hexdigest(),16))
    return int(f)

def getArea(s):
    n = (s % 30) * 100 + ((s % 5) * 5)
    while (n < 1000):
        n+=105
    return n

def getRm(s):
    n = s % 10
    if (n >= 5):
        n-=4
    if n == 1:
        n+=1
    if n == 0:
        n+=2
    return n

def getPrice(s):
    area = getArea(s)
    rms = getRm(s)
    intPrice =  (area * rms * rms * 50)
    locale.setlocale( locale.LC_ALL, '' )
    return locale.currency( intPrice, grouping=True )

def getRealtor(s):
    return realtors[s % len(realtors)]

def getSeller(s):
    return sellers[s % len(sellers)]

def getTaxRate(s):
    return taxRates[s % len(taxRates)]

def getCrimeRate(s):
    return crimeRates[s % len(crimeRates)]

def getFrequentCrime(s):
    return crimes[s % len(crimes)]

def getGeoIncident(s):
    return geo_incidents[s % len(geo_incidents)]

def getElemSchool(s):
    return elementarySchools[s % len(elementarySchools)]

def getHighSchool(s):
    return highSchools[s % len(highSchools)]

def getSchoolDis(s):
    return schoolDistricts[s % len(schoolDistricts)]

def getDate(s):
    return dates[s % len(dates)]

def generateListing(query):
    lis = Listing.query.filter_by(address=query).first()
    if lis:
        return lis

    s = ''.join(query.split())
    hashed = getHash(s)
    lis = Listing(address = query, area = getArea(hashed),price = getPrice(hashed),
                  bedrooms = getRm(hashed), bathrooms = (getRm(hashed) - 1),
                  realtor = getRealtor(hashed), seller = getSeller(hashed),
                  school_district = getSchoolDis(hashed));
    db.session.add(lis)
    tax = Tax(rate=getTaxRate(hashed), listing=lis)
    elemSchool = School(name=getElemSchool(hashed), listing=lis)
    highSchool = School(name=getHighSchool(hashed), listing=lis)
    crim = Crime(rate=getCrimeRate(hashed), most_frequent_crime=getFrequentCrime(hashed),
                listing=lis)
    geo = Geo(most_frequent_incident=getGeoIncident(hashed), most_recent_incident=getDate(hashed),
            listing=lis)
    db.session.add(tax)
    db.session.add(elemSchool)
    db.session.add(highSchool)
    db.session.add(crim)
    db.session.add(geo)
    db.session.commit()
    return lis
