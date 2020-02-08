Wrapper para a API de Cotação do Banco Central.

# Instalação

```bash
pip install pycotacao
```
# Exemplos

```python
>>> from pycotacao import get_exchange_rates, CurrencyCodes
# Obtenha dados de qualquer moeda.
...
>>> get_exchange_rates(CurrencyCodes.UYU)
UYU on 2020-02-07 at 13:17 (-0300) - BUY: 0.1145 / SELL: 0.1146.
# Inclusive de qualquer data.
...
>>> from datetime import datetime
>>> get_exchange_rates(CurrencyCodes.UYU, datetime(2000, 1, 1))
UYU on 1999-12-31 at 11:53 (-0200) - BUY: 0.152403 / SELL: 0.1544.
# Veja as taxas de compra e de venda do dia para cada moeda.
...
>>> get_exchange_rates(CurrencyCodes.USD).buying_rate
4.307
>>> get_exchange_rates(CurrencyCodes.USD).selling_rate
4.3076
# E converta para real...
...
>>> get_exchange_rates(CurrencyCodes.USD).currency_to_brl(53)
228.27100000000002
# ...ou o inverso também!
...
>>> get_exchange_rates(CurrencyCodes.USD).brl_to_currency(53)
12.303835082180333
```
# Limitações

Disponíveis na página do [Banco Central](https://www.bcb.gov.br/conversao).
> - O cálculo efetuado tem caráter informativo e não substitui as disposições da norma cambial brasileira para casos específicos de conversão.
> - Conversões disponíveis para datas informadas a partir de 01/02/1999.
> - Para dias não úteis, assume-se a cotação do dia útil imediatamente anterior.
> - O Banco Central não assume qualquer responsabilidade pela não simultaneidade ou falta das informações prestadas, assim como por eventuais erros de paridades das moedas, ou qualquer outro, salvo a paridade relativa ao dólar dos Estados Unidos da América em relação ao Real. Igualmente, não se responsabiliza pelos atrasos ou indisponibilidade de serviços de telecomunicação, interrupção, falha ou pelas imprecisões no fornecimento dos serviços ou informações. Não assume, também, responsabilidade por qualquer perda ou dano oriundo de tais interrupções, atrasos, falhas ou imperfeições, bem como pelo uso inadequado das informações contidas na transação.
