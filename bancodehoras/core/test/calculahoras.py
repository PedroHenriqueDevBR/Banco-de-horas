def calcular_hora(inicio, fim):
    if ':' not in inicio or ':' not in fim:
        return 0

    hora_inicio = converte_hora_em_minutos(inicio)
    hora_final = converte_hora_em_minutos(fim)

    if hora_inicio > hora_final:
        return 0
    else:
        return converter_minutos_em_horas(hora_final - hora_inicio)


def converte_hora_em_minutos(hora_completa):
    if ':' not in hora_completa:
        return 0
    
    horas = int(hora_completa.split(':')[0]) * 60
    minutos = int(hora_completa.split(':')[1])

    return horas + minutos


def converter_minutos_em_horas(minutos):
    if minutos > 60:
        horas = minutos // 60
        minutos = minutos - (horas * 60)
    else:
        horas = 0
        minutos

    return '{}:{}'.format(horas, minutos)
    


def main():
    hora_inicial = input('Digite a hora inicial: ')
    hora_final = input('Digite a hora final: ')
    print(calcular_hora(hora_inicial, hora_final))


if __name__ == '__main__':
    main()