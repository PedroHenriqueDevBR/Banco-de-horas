from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import xlwt


def main():
    print('Está funcionando')
    relatorio_de_usuarios_por_setor_pdf()
    print('Finalizou')


def relatorio_de_usuarios_por_setor(setor=None):
    pasta = 'arquivos/'
    nome_arquivo = 'relatorio.xls'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sequencia')

    titulos = ['nome','matricula','email']
    ws.write(0,0,titulos[0])
    ws.write(0,1,titulos[1])
    ws.write(0,2,titulos[2])

    linhas = []
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])
    linhas.append(['Pedro Henrique', '32595', 'pedro.ribeiro@grupovanguarda.com'])

    for i in range(len(linhas)):
        j = i + 1
        ws.write(j, 0, linhas[i][0])
        ws.write(j, 1, linhas[i][1])
        ws.write(j, 2, linhas[i][2])

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