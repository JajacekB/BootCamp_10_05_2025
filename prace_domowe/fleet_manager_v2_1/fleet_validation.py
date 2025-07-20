import re
import dns.resolver


def get_valid_phone() -> bool:
    patern = re.compile(r"^(\+\d{1,3}[ -]?)?\d{3}[ -]?\d{3}[ -]?\d{3}$")
    while True:
        phone = input("📱 Nr telefonu: ").strip()
        if patern.fullmatch(phone):
            # print("✅ Poprawny numer telefonu.")
            return phone
        else:
            print("❌ Niepoprawny format telefonu. Spróbuj jeszcze raz/")


def get_valid_email() -> str:
    while True:
        email = input("📧 Podaj adres e-mail: ").strip()
        if not is_valid_email_format(email):
            print("❌ Niepoprawny format adresu e-mail.")
            continue

        domain = email.split('@')[1]
        if not domain_has_mx_record(domain):
            print("❌ Domena e-mail nie istnieje lub nie obsługuje poczty.")
            continue

        print("✅ Poprawny e-mail i domena działa.")
        return email


def is_valid_email_format(email: str) -> bool:
    pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    return bool(pattern.match(email))


def domain_has_mx_record(domain: str) -> bool:
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
        return False