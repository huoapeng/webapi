class authentication_type:
    private = 1
    company = 2
    bank = 4
    alipay = 8

class verify_type:
    auto = 1
    manual = 2

class approval_result:
    deny = 1
    allow = 2

class bid_status:
    start = 1
    selectBidder = 2
    finish = 3

class file_type:
    profileLarge = 11
    profileMedium = 12
    profileSmall = 13
    version = 2
    privateFront = 3
    privateBack = 4
    companyLience = 5
    companyContactCard = 6
    work = 7
    workThumbnail = 8
    recommend = 9
    workFile = 51

class user_status:
    normal = 1
    disable = 2

class kind_status:
    normal = 1
    delete = 2

class project_status:
    normal = 1
    disable = 2
    delete = 3

class task_status:
    bidding = 1
    selectBidder = 2
    finish = 3
    disable = 4
    delete = 5

class version_status:
    normal = 1
    delete = 2
        
class note_status:
    normal = 1
    delete = 2

class message_type:
    version = 1
    note = 2
    work = 3

class work_status:
    normal = 1
    delete = 2

class copyright_type:
    none = 1
    attribution = 2
    attribution_non_commercial = 3
    attribution_no_derivative = 4
    attribution_share_alike = 5
    attribution_non_commercial_no_derivative = 6
    attribution_non_commercial_share_alike = 7


