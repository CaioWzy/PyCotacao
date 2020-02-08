import enum
import re
from datetime import datetime
from urllib import request
from urllib.error import HTTPError

from dateutil import parser

__all__ = [
    "CurrencyCodes",
    "PyCotacaoBaseException",
    "ExchangeRateNotFound",
    "get_exchange_rates",
]


@enum.unique
class CurrencyCodes(enum.Enum):
    """
    Enum of Currencies along with their identifier.
    Source https://www.bcb.gov.br/fis/pstaw10/Tabela_Moedas_CADIP.txt
    """

    AFN = 5
    ETB = 9
    THB = 15
    PAB = 20
    VES = 25
    BOB = 30
    GHS = 35
    CRC = 40
    SVC = 45
    NIO = 51
    DKK = 55
    EKK = 57
    SKK = 58
    ISK = 60
    NOK = 65
    SEK = 70
    CZK = 75
    GMD = 90
    DZD = 95
    KDW = 100
    BHD = 105
    IQD = 115
    JOD = 125
    LYD = 130
    MKD = 132
    RSD = 133
    SDG = 134
    TND = 135
    SDR = 138
    MAD = 139
    AED = 145
    STN = 148
    AUD = 150
    BSD = 155
    BMD = 160
    CAD = 165
    GYD = 170
    NAD = 173
    BBD = 175
    BZD = 180
    BND = 185
    KYD = 190
    SGD = 195
    FJD = 200
    HKD = 205
    TTD = 210
    XCD = 215
    ZWL = 217
    USD = 220
    JMD = 230
    LRD = 235
    NZD = 245
    SBD = 250
    VND = 260
    AMD = 275
    CVE = 295
    ANG = 325
    AWG = 328
    HUF = 345
    BIF = 365
    KMF = 368
    XOF = 370
    XPF = 380
    DJF = 390
    GNF = 398
    MGA = 405
    RWF = 420
    CHF = 425
    HTG = 440
    PYG = 450
    UAH = 460
    JPY = 470
    GEL = 482
    LVL = 485
    ALL = 490
    HNL = 495
    SLL = 500
    MDL = 503
    RON = 505
    BGN = 510
    GIP = 530
    EGP = 535
    GBP = 540
    LBP = 560
    SHP = 570
    SYP = 575
    SZL = 585
    TRY = 600
    LTL = 601
    LSL = 603
    AZN = 607
    BAM = 612
    MZN = 620
    ERN = 625
    NGN = 630
    AOA = 635
    TWD = 640
    PEN = 660
    BTN = 665
    TOP = 680
    MOP = 685
    ARS = 706
    CLP = 715
    COP = 720
    CUP = 725
    DOP = 730
    PHP = 735
    GWP = 738
    MXN = 741
    UYU = 745
    BWP = 755
    MWK = 760
    ZMW = 765
    GTQ = 770
    MMK = 775
    PGK = 778
    HRK = 779
    LAK = 780
    ZAR = 785
    BRL = 790
    CNY = 795
    QAR = 800
    OMR = 805
    YER = 810
    IRR = 815
    SAR = 820
    KHR = 825
    MYR = 828
    BYN = 829
    RUB = 830
    MUR = 840
    NPR = 845
    SCR = 850
    LKR = 855
    INR = 860
    IDR = 865
    MVR = 870
    PKR = 875
    ILS = 880
    UZS = 893
    BDT = 905
    WST = 911
    KZT = 913
    MNT = 915
    XEU = 918
    VUV = 920
    KPW = 925
    KRW = 930
    TZS = 946
    KES = 950
    UGX = 955
    SOS = 960
    PLN = 975
    EUR = 978


class Currency:
    """Currency class."""

    def __init__(self, currency_code, dt, buying_rate, selling_rate):
        self.__currency_code = currency_code
        self.__datetime = dt
        self.__buying_rate = buying_rate
        self.__selling_rate = selling_rate

    @property
    def currency_code(self):
        return self.__currency_code

    @property
    def datetime(self):
        """
        When was the data last updated at Banco Central.

        Returns
        -------
        datetime
            datetime object of the latest update.
        """
        return self.__datetime

    @property
    def buying_rate(self):
        """
        Returns
        -------
        float
        """
        return self.__buying_rate

    @property
    def selling_rate(self):
        """
        Returns
        -------
        float
        """
        return self.__selling_rate

    def currency_to_brl(self, amount):
        """
        Currency conversion to BRL.

        Params
        -------
        amount : int, float
            amount of money to exchange to BRL.

        Returns
        -------
        float
            Exchanged value to BRL.
        """
        if self.buying_rate > 0:
            return amount * self.buying_rate

    def brl_to_currency(self, amount):
        """
        Currency conversion from BRL.

        Params
        -------
        amount : int, float
            amount of money to exchange from BRL.

        Returns
        -------
        float
            Exchanged value to foreign currency.
        """
        if self.selling_rate > 0:
            return amount * (1 / self.selling_rate)

    def __repr__(self):
        fmt_datetime = self.datetime.strftime("%Y-%m-%d at %H:%M (%z)")
        return (
            f"{self.currency_code.name} on {fmt_datetime} "
            + f"- BUY: {self.buying_rate} / SELL: {self.selling_rate}."
        )


@enum.unique
class Patterns(enum.Enum):
    """Regex patterns for harvesting some data."""

    CODIGO_MOEDA = re.compile(r"<codigoMoeda>(\d{1,3})</codigoMoeda>")
    DATA_HORA_COTACAO = re.compile(
        r"<dataHoraCotacao>(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}-\d{4})</dataHoraCotacao>"
    )
    TAXA_COMPRA = re.compile(r"<taxaCompra>(\d+.\d{8})</taxaCompra>")
    TAXA_VENDA = re.compile(r"<taxaVenda>(\d+.\d{8})</taxaVenda>")


def __parse_response(xml_data):
    
    def parse_xml(pattern):
        match = re.search(pattern.value, xml_data)

        if match:
            return match.group(1)

    try:
        return {
            "dt": parser.isoparse(parse_xml(Patterns.DATA_HORA_COTACAO)),
            "buying_rate": float(parse_xml(Patterns.TAXA_COMPRA)),
            "selling_rate": float(parse_xml(Patterns.TAXA_VENDA)),
        }
    except TypeError:
        pass


class PyCotacaoBaseException(Exception):
    pass


class ExchangeRateNotFound(PyCotacaoBaseException):
    pass


def get_exchange_rates(currency_code, dt=datetime.today()):
    """
    Parameters
    ----------
    currency_code : CurrencyCodes
        CADIP currency code.
    dt : datetime
        Look up by date. You're allowed to get data from 1999-02-01.
    Returns
    -------
    Currency
        Currency object.

    """

    if dt > datetime.today():
        raise ValueError("Hey! You can't get exchange rates from the future.")

    elif dt < datetime(1999, 2, 1):
        raise ValueError("Can't get exchange rates for days older than 1999-02-01.")

    BASEURL = "https://www3.bcb.gov.br/bc_moeda/rest/cotacao/fechamento/ultima/1/"
    code = currency_code.value
    fmt_date = dt.strftime("%Y-%m-%d")

    try:
        with request.urlopen(BASEURL + f"{code}/{fmt_date}") as r:
            response = r.readline().decode("utf-8")
            response_data = __parse_response(response)

            if response_data:
                return Currency(currency_code=currency_code, **response_data)

    except HTTPError as ex:
        if ex.code == 404:
            raise ExchangeRateNotFound("No data found for that currency on that day.")
