import numpy as np


class Formatter:

    def __init__(self, rawDf):
        self.raw = rawDf
        self.raw['registrationRecognized'] = None
        self.raw['estimate'] = None
        self.raw['repriseFerme'] = None
        self.raw['estimationRegistration'] = None
        self.raw['repriseFermeRegistration'] = None
        self.raw['period'] = None
        self.raw['billingStatus'] = None
        self.raw["origin"] = self.raw.apply(getOriginDealer, axis=1)
        self.data = self.raw.apply(getRegistrationRecognized, axis=1).apply(
            getFilterValueRepriseFerme, axis=1).apply(
                getFilterValue, axis=1).apply(
                        getBillingStatus, axis=1).apply(
                    getPeriod, axis=1)
        rename = {"estimateValuationDate": "estimationDate"}
        self.data = self.data.rename(columns=rename)
        self.data = self.data.reindex(columns=column_names)

    def get(self) : 
        return self.data.rename(columns=finalNames)

    def resultShort(self):
        final = self.data.rename(columns=finalNames).drop_duplicates(subset=['WIDGET_NAME','UC_BRAND', 'UC_MODEL',
                                                                             'UC_FUEL', 'UC_VERSION', 'BRAND',
                                                                             'COUNTRY', 'UC_REGISTRATION_DATE',
                                                                             'CURRENT_MILEAGE', 'PERIOD'], keep='first')
        return final #[shortListColumns]


def getRecordType(row):
    status = row["status"]
    lastStep = row["lastStepVisited"]
    estimateAccepted = row["estimateAccepted"]
    if status >= 200 and estimateAccepted == 'yes':
        return 'recoveryFermeestimate'
    if 'engagement' in lastStep:
        return 'recoveryFerme'
    if 'estimate' in lastStep:
        return 'estimate'
    return None


def getRegistrationRecognized(row):
    if row['userAction'] == 'closed' or row['regNumber'] is None or row['regNumber'] is np.nan:
        row["registrationRecognized"] = None
    elif row['userAction'] == 'engagement-carSummary-error' or row['userAction'] == 'version-estimate-error':
        row["registrationRecognized"] = 'Yes'
    else:
        row["registrationRecognized"] = "No"
    return row


def getFilterValueRepriseFerme(row):
    registrationRecognized = row["registrationRecognized"]
    repriseFermeStep = [
        'engagement-your-valuation',
        'upload-photo',
        'engagement-feedback',
    ]
    repriseFermeStepRegistration = [
        'engagement-carSummary',
        'engagement-carDetails',
        'engagement-version',
        'engagement-feedback',
        'engagement-your-valuation',
        'upload-photo',
    ]
    if row['lastStepVisited'] in repriseFermeStepRegistration and registrationRecognized in ['Non', 'No']:
        row['repriseFermeRegistration'] = 'Yes'
    else:
        row['repriseFermeRegistration'] = 'No'
    if row['lastStepVisited'] in repriseFermeStep and registrationRecognized in ['Non', 'No']:
        row['repriseFerme'] = 'Yes '
    else:
        row['repriseFerme'] = 'No '

    return row


def getFilterValue(row):
    registrationRecognized = row["registrationRecognized"]

    repriseEstimateStepRegistration = [
        'estimate-carDetails',
        'estimate-version',
        'estimate-your-valuation',
    ]
    recordType = getRecordType(row)
    row["type"] = recordType
    if recordType is None:
        row['estimate'] = None
        row['repriseFerme'] = None
        row['estimationRegistration'] = None
        row['repriseFermeRegistration'] = None

    if recordType == 'recoveryFerme':
        row['estimate'] = None
        row['estimationRegistration'] = None
        # row['repriseFerme'] = $resultRepriseFerme['repriseFerme'] ;
        # $result['repriseFermeRegistration'] = $resultRepriseFerme['repriseFermeRegistration'];

    if recordType == 'estimate':
        row['repriseFerme'] = None
        row['repriseFermeRegistration'] = None
        if row['lastStepVisited'] in repriseEstimateStepRegistration and registrationRecognized in ["Non", "No"]:
            row['estimationRegistration'] = 'Yes '
        else:
            row['estimationRegistration'] = 'No '

        if row['lastStepVisited'] == 'estimate-your-valuation' and registrationRecognized in ['Non', 'No']:
            row['estimate'] = 'Yes '
        else:
            row['estimate'] = 'No '

        if recordType == 'recoveryFermeEstimate':
            row['estimate'] = 'Yes '
            row['estimationRegistration'] = 'Yes '
            # $resultRepriseFerme = $this->getFilterValueRepriseFerme($record, $registrationRecognized);
            # $result['repriseFerme'] = $resultRepriseFerme['repriseFerme'];
            # $result['repriseFermeRegistration'] = $resultRepriseFerme['repriseFermeRegistration'];

    return row


def getOriginDealer(row):
    brand = row['brandMop']
    type = row['typeMop']
    if type == 'AVNVCG' or type == 'ACVNVCG':
        return 'VCG'
    if type == 'AVNSR':
        return "STK"
    if type == 'ACVNR':
        return 'B2C'
    if type == 'ACVNRPRO':
        return "B2B"
    if type == 'EDL' and brand == 'AC':
        return 'C3J'
    if type == 'EDL' and brand == 'DS':
        return "DS3"
    return 'N/A'


def getPeriod(row):
    row["period"] = row["creationAt"].strftime("%Y%m")
    return row


def getBillingStatus(row):

    row["billingStatus"] = billingStatus(
        row["lastStepVisited"], row["registrationRecognized"])
    return row

def billingStatus(lastStepVisited, registrationRecognized):
    if lastStepVisited == 'estimate-your-valuation':
        return "SIMPLE_VALUATION"
    if lastStepVisited in ["engagement-your-valuation", "engagement-feedback", "upload-photo"]:
        return "FULL_VALUATION"
    if lastStepVisited in ["estimate-carDetails", "estimate-version", "estimate-your-valuation"] and registrationRecognized == "No":
        return "LICENSEPLATE_SIMPLE_VALUATION"
    if lastStepVisited in ["engagement-car-state/accident", "engagement-car-state/defect", "engagement-car-state/equipment", "engagement-car-state/immobilize", "engagement-car-state/imported", "engagement-car-state/maintenance", "engagement-car-state/mileage", "engagement-car-state/owner", "engagement-car-state/pledged", "engagement-car-state/technicalControl", "engagement-car-state/tires", "engagement-carSummary", "engagement-version", "engagement-legal-notice", "engagement-feedback", "engagement-your-valuation", "upload-photo"] and registrationRecognized == "No":
        return "LICENSEPLATE_FULL_VALUATION"

finalNames = {"widgetName": "WIDGET_NAME",
              "creationAt": "CREATION_DATE",
              "chronoId": "CHRONO_NUMBER",
              "mopId": "MOP_ID",
              "apiKey": "WIDGET_KEY",
              "origin": "WIDGET_CLIENT",
              "brand": "BRAND",
              "country": "COUNTRY",
              "status": "STATUS_ID",
              "label": "STATUS_LABEL",
              "lastStepVisited": "LAST_VISITED_STEP",
              "estimationDate": "ESTIMATION_DATE",
              "estimateAccepted": "ESTIMATION_ACCEPTED",
              "valuationDate": "ENGAGEMENT_DATE",
              "accepted": "ENGAGEMENT_ACCEPTED",
              "uploadDate": "UPLOAD_DATE",
              "makeName": "UC_BRAND",
              "modelName": "UC_MODEL",
              "fuelTypeName": "UC_FUEL",
              "versionName": "UC_VERSION",
              "firstRegistration": "UC_REGISTRATION_DATE",
              "overallMileage": "CURRENT_MILEAGE",
              "annualMileage": "ANNUAL_MILEAGE",
              "expectedMileage": "DELIVERY_DATE_EXPECTED_MILEAGE",
              # "" : "DELIVERY_DATE_REAL_MILEAGE",
              "excluded": "EXCLUDED",
              "registrationCertificateName": "OWNERSHIP",
              "pledged": "PLEDGE",
              "roll": "RUNNING",
              "state": "SALVAGE",
              "import": "IMPORT",
              "technicalControl": "INSPECTION",
              "frontTiresCondition": "FRONT_TIRES_STATE",
              "rearTiresCondition": "REAR_TIRES_STATE",
              "mechanicalCondition": "MECHANICAL_STATE",
              "electronicCondition": "EQUIPMENT_STATE",
              "serviceHistory": "SERVICE_HISTORY",
              "interiorCondition": "INTERIOR_STATE",
              "damage": "DAMAGE_NUMBER",
              "answer": "FEEDBACK_ANSWER",
              "estimateValuationApplied": "ESTIMATION_OFFER",
              "estimatedFrevoStat": "STATISTICAL_RECON_COSTS_ESTIMATION",
              "frevoStat": "STATISTICAL_RECON_COSTS_ENGAGEMENT",
              "frevoDamage": "DECLARED_RECON_COSTS",
              "quotation": "ENGAGEMENT_OFFER_BEFORE_RECON_COSTS",
              "valuationApplied": "ENGAGEMENT_OFFER_AFTER_RECON_COSTS",
              "eligibility": "ELIGIBLE_TO_CONVERSION_PREMIUM",
              "amount": "BRAND_CONTRIBUTION",
              "commercial": "NC_NAME",
              "priceVn": "NC_PRICE",
              "availibilityDate": "NC_DELIVERY_DATE",
              "address" : "address",
              # adress - "name" : "DEALERSHIP_NAME",
              # "addresszipCodephone" : "DEALERSHIP_ADDRESS",
              # "" : "DEALERSHIP_ZIP_CODE",
              # "" : "DEALERSHIP_PHONE_NUMBER",
              "rrdiCode": "DEALERSHIP_RRDI_CODE",
              "userAction": "TEST",
              "duplicateInd": "DUPLICATE",
              "registrationRecognized": "IMMAT_NOT_RECOGNIZED",
              "estimate": "SIMPLE_VALUATION",
              "estimationRegistration": "FULL_VALUATION",
              "repriseFerme": "LICENSEPLATE_SIMPLE_VALUATION",
              "repriseFermeRegistration": "LICENSEPLATE_FULL_VALUATION",
              "middlewareTrack": "SEND_LEAD",
              "creationHour": "CREATION_HOUR",
              "medianInd": "NO_MEDIAN",
              "valuationKey": "VALUATION_KEY",
              "updatedAt": "UPDATED_AT",
              "period": "PERIOD",
              "billingStatus": "BILLING_STATUS"
              }

shortListColumns = [
    "WIDGET_NAME", "CREATION_DATE", "CHRONO_NUMBER", "MOP_ID", "WIDGET_KEY", "WIDGET_CLIENT", "BRAND", "COUNTRY", "STATUS_ID", "STATUS_LABEL", "LAST_VISITED_STEP", "ESTIMATION_DATE", "ESTIMATION_ACCEPTED", "ENGAGEMENT_DATE", "ENGAGEMENT_ACCEPTED", "UPLOAD_DATE", "UC_BRAND", "UC_MODEL", "UC_FUEL", "UC_VERSION", "UC_REGISTRATION_DATE", "CURRENT_MILEAGE", "FEEDBACK_ANSWER", "ESTIMATION_OFFER", "TEST", "DUPLICATE", "IMMAT_NOT_RECOGNIZED", "SIMPLE_VALUATION", "FULL_VALUATION", "LICENSEPLATE_SIMPLE_VALUATION", "LICENSEPLATE_FULL_VALUATION", "VALUATION_KEY", "PERIOD", "BILLING_STATUS", "CREATION_HOUR", "SEND_LEAD", "DUPLICATE", "DELIVERY_DATE_EXPECTED_MILEAGE"
]

column_names = ["widgetName", "creationAt", "chronoId", "mopId", "apiKey",
                "origin", "brand", "country", "status", "label", "lastStepVisited",
                "estimationDate", "estimateAccepted", "valuationDate", "accepted",
                "uploadDate",  "makeName", "modelName", "fuelTypeName", "versionName",
                "firstRegistration", "overallMileage", "annualMileage", "expectedMileage",
                "excluded", "registrationCertificateName", "pledged", "roll", "state", "import",
                "technicalControl", "frontTiresCondition", "rearTiresCondition", "mechanicalCondition",
                "electronicCondition", "serviceHistory", "interiorCondition", "damage", "answer",
                "estimateValuationApplied", "estimatedFrevoStat", "frevoStat", "frevoDamage",
                "quotation", "valuationApplied", "eligibility", "amount", "commercial", "priceVn",
                "availibilityDate", "address", "rrdiCode", "userAction",
                "duplicateInd", "registrationRecognized", "estimate", "repriseFerme", "estimationRegistration", "repriseFermeRegistration",
                "middlewareTrack", "creationHour", "medianInd", "valuationKey" ,"updatedAt","period", "billingStatus"
                ]
