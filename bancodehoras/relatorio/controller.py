from core.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import xlwt


def main():
    print('Está funcionando')
    relatorio_de_usuarios_por_setor()
    print('Finalizou')


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


def relatorio_de_usuarios_por_setor_pdf():
    pasta = 'arquivos/'
    nome_arquivo = 'relatorio.pdf'

    cnv = canvas.Canvas(pasta + nome_arquivo, pagesize=A4)
    width, height = A4

    px = mm2p(100)
    py = mm2p(150)

    cnv.drawString(px, py, "Pedro Henrique")
    cnv.save()


if __name__ == '__main__':
    main()