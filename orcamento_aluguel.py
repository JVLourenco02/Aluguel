import csv

class OrcamentoAluguel:
    def __init__(self):
        # Valores padrão das locações (1 Quarto)
        self.valores_base = {
            "1": {"tipo": "Apartamento", "valor": 700.00},
            "2": {"tipo": "Casa", "valor": 900.00},
            "3": {"tipo": "Estudio", "valor": 1200.00}
        }
        self.valor_contrato_total = 2000.00

    def calcular_orcamento(self):
        print("=== SISTEMA DE ORÇAMENTO - IMOBILIÁRIA R.M ===")
        print("Selecione o tipo de imóvel:")
        print("1 - Apartamento (R$ 700,00 base)")
        print("2 - Casa (R$ 900,00 base)")
        print("3 - Estúdio (R$ 1200,00 base)")
        
        opcao = input("Opção desejada (1, 2 ou 3): ")
        if opcao not in self.valores_base:
            print("Opção inválida! Encerrando.")
            return

        tipo_imovel = self.valores_base[opcao]["tipo"]
        mensalidade = self.valores_base[opcao]["valor"]

        # Regras para Apartamentos e Casas (Quartos e Garagem)
        if opcao in ["1", "2"]:
            quartos = input("Deseja 1 ou 2 quartos? (Digite 1 ou 2): ")
            if quartos == "2":
                if opcao == "1":
                    mensalidade += 200.00  # Adicional apto 2 quartos
                else:
                    mensalidade += 250.00  # Adicional casa 2 quartos
            
            garagem = input("Deseja incluir vaga de garagem? (S/N): ").strip().upper()
            if garagem == "S":
                mensalidade += 300.00

            # Desconto de 5% para apto sem crianças
            if opcao == "1":
                tem_criancas = input("O morador possui crianças? (S/N): ").strip().upper()
                if tem_criancas == "N":
                    mensalidade *= 0.95  # Aplica 5% de desconto

        # Regras para Estúdio (Vagas de Estacionamento)
        elif opcao == "3":
            estacionamento = input("Deseja adicionar vagas de estacionamento? (S/N): ").strip().upper()
            if estacionamento == "S":
                # Primeira contratação: R$ 250,00 por 2 vagas
                mensalidade += 250.00
                vagas_extras = int(input("Deseja adicionar mais quantas vagas extras? (R$ 60,00 cada. Digite 0 se não quiser): "))
                mensalidade += (vagas_extras * 60.00)

        # Parcelamento do Contrato
        print(f"\nO valor do contrato imobiliário é de R$ {self.valor_contrato_total:.2f}.")
        parcelas_contrato = int(input("Em quantas vezes deseja parcelar o contrato? (De 1 a 5 vezes): "))
        if parcelas_contrato < 1 or parcelas_contrato > 5:
            print("Número de parcelas inválido. Definido para 1 vez.")
            parcelas_contrato = 1

        valor_parcela_contrato = self.valor_contrato_total / parcelas_contrato

        # Exibição dos resultados na tela
        print("\n" + "="*40)
        print("          RESUMO DO ORÇAMENTO")
        print("="*40)
        print(f"Imóvel selecionado: {tipo_imovel}")
        print(f"Valor do Aluguel Mensal: R$ {mensalidade:.2f}")
        print(f"Contrato: {parcelas_contrato}x de R$ {valor_parcela_contrato:.2f}")
        print("="*40)

        # Geração do arquivo CSV com as 12 parcelas do ano
        self.gerar_csv(tipo_imovel, mensalidade, parcelas_contrato, valor_parcela_contrato)

    def gerar_csv(self, tipo, valor_aluguel, qtd_parcelas_contrato, valor_parc_contrato):
        nome_arquivo = "orcamento_aluguel.csv"
        
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            # Cabeçalho
            escritor.writerow(["Mês", "Tipo de Imóvel", "Valor Aluguel (R$)", "Parcela Contrato (R$)", "Total Mensal (R$)"])
            
            # Gerar as 12 linhas correspondentes aos 12 meses do orçamento
            for mes in range(1, 13):
                # O contrato só é somado nos primeiros meses correspondentes ao parcelamento escolhido
                contrato_no_mes = valor_parc_contrato if mes <= qtd_parcelas_contrato else 0.0
                total_mes = valor_aluguel + contrato_no_mes
                
                escritor.writerow([
                    f"Mês {mes}",
                    tipo,
                    f"{valor_aluguel:.2f}",
                    f"{contrato_no_mes:.2f}",
                    f"{total_mes:.2f}"
                ])
                
        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso com as 12 parcelas!")

# Execução do programa
if __name__ == "__main__":
    app = OrcamentoAluguel()
    app.calcular_orcamento()