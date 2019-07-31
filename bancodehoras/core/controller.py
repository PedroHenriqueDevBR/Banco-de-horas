class FormataDados:
    def calcular_hora(self, inicio, fim):
        if ':' not in inicio or ':' not in fim:
            return 0

        hora_inicio = self.converte_hora_em_minutos(inicio)
        hora_final = self.converte_hora_em_minutos(fim)

        if hora_inicio > hora_final:
            return 0
        else:
            return self.converter_minutos_em_horas(hora_final - hora_inicio)


    def converte_hora_em_minutos(self, hora_completa):
        if ':' not in hora_completa:
            return 0
        
        horas = int(hora_completa.split(':')[0]) * 60
        minutos = int(hora_completa.split(':')[1])

        return horas + minutos


    def converter_minutos_em_horas(self, minutos):
        if minutos >= 60:
            horas = minutos // 60
            minutos = minutos - (horas * 60)
        else:
            horas = 0
            minutos

        hora_str = '{}'.format(horas)
        if horas < 10:
            hora_str = '0{}'.format(horas)

        min_str = '{}'.format(minutos)
        if minutos < 10:
            min_str = '0{}'.format(minutos)

        return '{}:{}'.format(hora_str, min_str)

    def calcular_total_de_horas(self, obj):
        total_min = 0
        # import pdb; pdb.set_trace()
        for movimentacao in obj:
            total_min += self.converte_hora_em_minutos(movimentacao.hora_total)
        return self.converter_minutos_em_horas(total_min)