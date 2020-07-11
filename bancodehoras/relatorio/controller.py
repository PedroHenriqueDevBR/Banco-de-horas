from core.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import xlwt


def main():
    print('Está funcionando')
    relatorio_de_usuarios_por_setor()
    print('Finalizou')

'''
dados = {
    titulos: ['nome', 'idade'],
    linhas: [
        [
            'pedro', 21
        ],
        [
            'Henrique', 21
        ],
        [
            'Carla', 17
        ]
    ]
}
'''


def gera_relatorio(dados, nome):
    pasta = 'relatorio/arquivos/'
    nome_arquivo = '{}.xls'.format(nome)
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Relatorio')

    titulos = dados['titulos']
    linhas = dados['linhas']

    # Gerar titulos
    for i in range(len(titulos)):
        ws.write(0, i, titulos[i])

    # Gera dados da tabela
    for i in range(len(linhas)):
        linha = linhas[i]
        for j in range(len(linha)):
            ws.write(i+1, j, linha[j])

    wb.save(pasta + nome_arquivo)


# Arquivos Excel
def relatorio_de_usuarios_por_setor(perfis=None):
    pasta = 'relatorio/arquivos/'
    nome_arquivo = 'relatorio.xls'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sequencia')

    titulos = ['nome','matricula','email', 'primeira CH', 'segunda CH', 'setor']
    ws.write(0,0,titulos[0])
    ws.write(0,1,titulos[1])
    ws.write(0,2,titulos[2])
    ws.write(0,3,titulos[3])
    ws.write(0,4,titulos[4])
    ws.write(0,5,titulos[5])

    linhas = []
    # linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com', '05:00', '05:00', 'TI'])

    if perfis is None:
        for perfil in perfis:
            linhas.append(
                [perfil.nome, perfil.usuario.username, perfil.usuario.email, perfil.ch_primeira, perfil.ch_segunda, perfil.setor.nome]
            )
    else:
        for perfil in Perfil.objects.all():
            linhas.append(
                [perfil.nome, perfil.usuario.username, perfil.usuario.email, perfil.ch_primeira, perfil.ch_segunda, perfil.setor.nome]
            )


    for i in range(len(linhas)):
        j = i + 1
        ws.write(j, 0, linhas[i][0])
        ws.write(j, 1, linhas[i][1])
        ws.write(j, 2, linhas[i][2])
        ws.write(j, 3, linhas[i][3])
        ws.write(j, 4, linhas[i][4])
        ws.write(j, 5, linhas[i][5])

    wb.save(pasta + nome_arquivo)


def relatorio_solicitacoes_pendentes_do_perfil(perfil):
    solicitacoes = perfil.movimentacoes.all()
    resultado = []
    pasta = 'relatorio/arquivos/'
    nome_arquivo = 'minhas_solicitacoes.xls'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Resultado')
    
    for solicitacao in solicitacoes:
        resultado.append([
            str(solicitacao.data_cadastro),
            str(solicitacao.data_movimentacao),
            str(solicitacao.hora_inicial),
            str(solicitacao.hora_final),
            str(solicitacao.hora_total),
            solicitacao.motivo,
            solicitacao.status.nome
        ])
    
    titulo = ['Data da solicitacao', 'Data do evento', 'hora inicio', 'hora termino', 'total de horas', 'motivo', 'status']
    for i in range(len(titulo)):
        ws.write(0,i,titulo[i])

    for i in range(len(resultado)):
        j = i + 1
        ws.write(j,0,resultado[i][0])
        ws.write(j,1,resultado[i][1])
        ws.write(j,2,resultado[i][2])
        ws.write(j,3,resultado[i][3])
        ws.write(j,4,resultado[i][4])
        ws.write(j,5,resultado[i][5])
        ws.write(j,6,resultado[i][6])
    
    wb.save(pasta + nome_arquivo)


def relatorio_solicitacoes_do_meu_setor(perfis):
    resultado = []
    pasta = 'relatorio/arquivos/'
    nome_arquivo = 'solicitacoes_do_setor.xls'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Resultado')

    titulo = ['Colaborador', 'Data da solicitacao', 'Data do evento', 'hora inicio', 'hora termino', 'total de horas', 'motivo', 'status']
    for i in range(len(titulo)):
        ws.write(0,i,titulo[i])

    # formatando resultado
    for perfil in perfis:
        for movimentacao in perfil.movimentacoes.all():
            resultado.append([
                perfil.nome,
                str(movimentacao.data_cadastro),
                str(movimentacao.data_movimentacao),
                str(movimentacao.hora_inicial),
                str(movimentacao.hora_final),
                str(movimentacao.hora_total),
                movimentacao.motivo,
                movimentacao.status.nome
            ])

    for i in range(len(resultado)):
        j = i + 1
        ws.write(j,0,resultado[i][0])
        ws.write(j,1,resultado[i][1])
        ws.write(j,2,resultado[i][2])
        ws.write(j,3,resultado[i][3])
        ws.write(j,4,resultado[i][4])
        ws.write(j,5,resultado[i][5])
        ws.write(j,6,resultado[i][6])
        ws.write(j,7,resultado[i][7])
    
    wb.save(pasta + nome_arquivo)


# Arquivos PDF
def relatorio_de_usuarios_por_setor_pdf():
    pasta = 'arquivos/'
    nome_arquivo = 'relatorio.pdf'

    cnv = canvas.Canvas(pasta + nome_arquivo, pagesize=A4)
    width, height = A4

    px = mm2p(100)
    py = mm2p(150)

    cnv.drawString(px, py, "Pedro Henrique")
    cnv.save()


def gera_log(msg):
    print('\n' + '='*40)
    print(msg)
    print('='*40 + '\n')


if __name__ == '__main__':
    main()