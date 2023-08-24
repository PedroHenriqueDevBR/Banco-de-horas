from apps.core.models import Hash
from apps.movimentacao.controller import FuncionalidadesMovimentacao
from apps.usuario.models import Perfil


class FuncionalidadesCore:
    def formata_dados_do_grafico(self, perfil_arg: Perfil):
        movimentacao_func = FuncionalidadesMovimentacao([], [])
        perfis = perfil_arg.setor.perfis_do_setor.all()
        resultado = []

        for perfil in perfis:
            bancos = perfil.movimentacoes.filter(
                entrada=True,
                status=autorizado,
            )
            baixas = perfil.movimentacoes.filter(
                entrada=False,
                status=autorizado,
            )
            resultado.append(
                {
                    "nome": perfil.nome,
                    "total_horas": int(
                        movimentacao_func.total_de_horas_disponivel_do_perfil(
                            autorizado,
                            bancos,
                            baixas,
                        ).split(":")[0],
                    ),
                }
            )

        return resultado

    def hash_add(self, chave, valor):
        if self.hash_valid(chave, valor):
            return False
        else:
            Hash.objects.create(chave=chave, valor=valor)
            return True

    def hash_get(self, chave):
        valor = None
        try:
            valor = Hash.objects.filter(chave=chave)[0].valor
        except Exception:
            print("Chave inválida")
        return valor

    def hash_edit(self, objeto=None, chave=None, valor=None):
        if objeto is not None:
            objeto.valor = valor
            objeto.save()
            return True
        else:
            if self.hash_valid(chave, valor):
                try:
                    hash_obj = Hash.objects.filter(chave=chave)[0]
                    hash_obj.valor = valor
                    return True
                except Exception:
                    return False

            return False

    def hash_valid(self, chave, valor):
        return len(chave) > 0 and len(valor) > 0

    def superuser(self, request):
        return request.user.is_superuser

    def administardor(self, request):
        return request.user.perfil.gerente

    def superadministrador(self, request):
        return request.user.is_superuser and request.user.perfil.gerente
