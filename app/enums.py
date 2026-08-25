import enum


class AuthProvider(str, enum.Enum):
    LINKEDIN = "linkedin"
    GOOGLE = "google"
    EMAIL = "email"


class UserRole(str, enum.Enum):
    CANDIDATE = "candidate"
    REFERRER = "referrer"
    BOTH = "both"


class ActiveRole(str, enum.Enum):
    CANDIDATE = "candidate"
    REFERRER = "referrer"


class Availability(str, enum.Enum):
    LOOKING = "looking"
    NOT_LOOKING = "not_looking"


class ReferralListingStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class ReferralRequestStatus(str, enum.Enum):
    """Canonical referral tracking statuses."""

    REQUESTED = "requested"
    ACCEPTED = "accepted"
    SUBMITTED = "submitted"
    APPLICATION_RECEIVED = "application_received"
    RECRUITER_REVIEWING = "recruiter_reviewing"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_RECEIVED = "offer_received"
    OFFER_ACCEPTED = "offer_accepted"
    JOINED = "joined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


TERMINAL_STATUSES = {ReferralRequestStatus.REJECTED, ReferralRequestStatus.WITHDRAWN}

STATUS_FLOW = [
    ReferralRequestStatus.REQUESTED,
    ReferralRequestStatus.ACCEPTED,
    ReferralRequestStatus.SUBMITTED,
    ReferralRequestStatus.APPLICATION_RECEIVED,
    ReferralRequestStatus.RECRUITER_REVIEWING,
    ReferralRequestStatus.INTERVIEW_SCHEDULED,
    ReferralRequestStatus.INTERVIEW_COMPLETED,
    ReferralRequestStatus.OFFER_RECEIVED,
    ReferralRequestStatus.OFFER_ACCEPTED,
    ReferralRequestStatus.JOINED,
]


class EndorsementStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class NotificationType(str, enum.Enum):
    REFERRAL_ACCEPTED = "referral_accepted"
    REFERRAL_DECLINED = "referral_declined"
    STATUS_UPDATE = "status_update"
    INTERVIEW = "interview"
    OFFER = "offer"
    ENDORSEMENT = "endorsement"
    MATCHING_REFERRAL = "matching_referral"
    GENERAL = "general"
