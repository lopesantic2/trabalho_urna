import pickle
from colorama import Fore, Style

def obter_nome_cargo(codigo_cargo):
    """
        Função que retorna o nome completo de um cargo com base no código do cargo.

        Parâmetros:
        - codigo_cargo: Código do cargo (F, E, S, G, P).

        Retorna:
        - Nome completo do cargo.
        """
    if codigo_cargo == "F":
        return "Deputado Federal"
    elif codigo_cargo == "E":
        return "Deputado Estadual"
    elif codigo_cargo == "S":
        return "Senador"
    elif codigo_cargo == "G":
        return "Governador"
    elif codigo_cargo == "P":
        return "Presidente"
    else:
        return "Cargo Desconhecido"

def ler_arquivo_candidatos():
    """
       Função que lê um arquivo de candidatos e retorna uma lista de candidatos.

       Solicita o caminho do arquivo ao usuário.

       Retorna:
       - Lista de dicionários representando candidatos.
       """
    candidatos_lista = []
    caminho_arquivo = input("Informe a localização dos dados dos candidatos: ")

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(',')
                if len(dados) >= 6:
                    candidato = {
                        'nome': dados[1].strip(),
                        'numero': dados[2].strip(),
                        'partido': dados[3].strip(),
                        'estado': dados[4].strip(),
                        'cargo': dados[5].strip(),
                        'cargo_completo': obter_nome_cargo(dados[5].strip())
                    }
                    candidatos_lista.append(candidato)
        print("Arquivo de candidatos lido com sucesso.")
        return candidatos_lista
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return []

def ler_arquivo_eleitores():
    """
       Função que lê um arquivo de eleitores e retorna uma lista de eleitores.

       Solicita o caminho do arquivo ao usuário.

       Retorna:
       - Lista de dicionários representando eleitores.
       """
    eleitores_lista = []
    caminho_arquivo = input("Informe a localização dos dados dos eleitores: ")

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(',')
                if len(dados) >= 5:
                    eleitor = {
                        'nome': dados[1].strip(),
                        'rg': dados[2].strip(),
                        'titulo_eleitor': dados[3].strip(),
                        'municipio': dados[4].strip(),
                        'estado': dados[5].strip()
                    }
                    eleitores_lista.append(eleitor)
        print("Arquivo de eleitores lido com sucesso.")
        return eleitores_lista
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return []

def coletar_votos(candidatos_lista, eleitores_lista, estado_urna):
    """
        Função para coletar votos dos eleitores.

        Parâmetros:
        - candidatos_lista: Lista de candidatos.
        - eleitores_lista: Lista de eleitores.
        - estado_urna: Estado onde a urna está localizada.

        Retorna:
        - Dicionário contendo a apuração dos votos.
        """
    votos_apuracao = {'UF': estado_urna, 'Votos': []}

    while True:
        numero_titulo_eleitor = input("Informe o número do título de eleitor (ou 'FIM' para encerrar a votação): ")

        if numero_titulo_eleitor.upper() == 'FIM':
            break

        eleitor = next((e for e in eleitores_lista if e['titulo_eleitor'] == numero_titulo_eleitor), None)

        if eleitor:
            print(f"\nEleitor: {eleitor['nome']} | Estado: {eleitor['estado']}")
            estado = eleitor['estado']

            votos_eleitor = {'UF': estado_urna, 'Votos': []}

            for cargo in ["F", "E", "S", "G", "P"]:
                while True:
                    voto = input(f"Informe o voto para {obter_nome_cargo(cargo)} (ou 'B' para voto em branco, 'N' para voto nulo): ").strip()
                    voto_candidato = None

                    if voto.upper() == 'B':
                        voto_candidato = {'Cargo': cargo, 'Voto': 'Branco'}
                        break
                    elif voto.upper() == 'N':
                        voto_candidato = {'Cargo': cargo, 'Voto': 'Nulo'}
                        break
                    else:
                        candidato = None

                        if cargo == "P":
                            candidato = next((c for c in candidatos_lista if c['cargo'] == cargo and c['numero'] == voto), None)
                        else:
                            candidatos_estado = [c for c in candidatos_lista if c['cargo'] == cargo and str(c['estado']) == estado_urna]
                            candidato = next((c for c in candidatos_estado if c['numero'] == voto), None)

                        if candidato:
                            print(f"Candidato {obter_nome_cargo(cargo)}: {candidato['nome']} | {candidato['partido']}")
                            confirmacao = input("Confirma (S ou N)? ").upper()
                            if confirmacao == 'S':
                                voto_candidato = {'Cargo': cargo, 'Voto': str(voto)}
                                break
                            elif confirmacao == 'N':
                                print("Por favor, insira novamente o número do candidato.")
                        else:
                            print("Número do candidato incorreto. Por favor, insira novamente.")

                votos_eleitor['Votos'].append(voto_candidato)
                print("\nVoto registrado com sucesso!\n")

            votos_apuracao['Votos'].append(votos_eleitor)

    with open('votos_salvos.pkl', 'ab') as arquivo:
        pickle.dump(votos_apuracao, arquivo)

    return votos_apuracao


def salvar_votos(votos):
    """
      Função para salvar os votos em um arquivo pickle.

      Parâmetros:
      - votos: Dicionário contendo a apuração dos votos.
      """
    with open('votos_salvos.pkl', 'wb') as arquivo:
        pickle.dump(votos, arquivo)


def apurar_votos():
    """
        Função para apurar os votos salvos em um arquivo pickle.

        Retorna:
        - Lista de dicionários contendo a apuração dos votos.
        """
    votos_salvos = []

    try:
        with open('votos_salvos.pkl', 'rb') as arquivo:
            while True:
                try:
                    voto = pickle.load(arquivo)
                    votos_salvos.append(voto)
                except EOFError:
                    break

        if not votos_salvos:
            print("Não há votos apurados. Realize a votação e apuração antes de mostrar os resultados.")
        else:
            print("Votos apurados:")
            for votos_estado in votos_salvos:
                print(votos_estado)
            return votos_salvos

    except FileNotFoundError:
        print("Não há votos apurados. Realize a votação e apuração antes de mostrar os resultados.")
        return []



def gerar_boletim_urna(apuracao, candidatos_lista):
    """
       Função para gerar um boletim de urna com base na apuração dos votos.

       Parâmetros:
       - apuracao: Lista de dicionários contendo a apuração dos votos.
       - candidatos_lista: Lista de candidatos.
       """
    with open('boletim_urna.txt', 'w', encoding='utf-8') as arquivo:
        for apuracao_estado in apuracao:
            estado = apuracao_estado.get('UF', '')
            votos_estado = apuracao_estado.get('Votos', [])

            if estado:
                eleitores_aptos = len(votos_estado)
                arquivo.write(f"\nApuração dos votos no estado {estado}:\nEleitores Aptos: {eleitores_aptos}\n")

                votos_nominais = [voto for eleitor in votos_estado for voto in eleitor['Votos'] if voto['Voto'] not in ['Branco', 'Nulo']]
                brancos = [voto for eleitor in votos_estado for voto in eleitor['Votos'] if voto['Voto'] == 'Branco']
                nulos = [voto for eleitor in votos_estado for voto in eleitor['Votos'] if voto['Voto'] == 'Nulo']

                total_votos_nominais = len(votos_nominais)

                arquivo.write(f"Total de Votos Nominais: {total_votos_nominais}\n")
                arquivo.write(f"Brancos: {len(brancos)}\n")
                arquivo.write(f"Nulos: {len(nulos)}\n")

                arquivo.write("\nResultados:\n")

                for candidato in candidatos_lista:
                    cargo, numero = candidato['cargo'], candidato['numero']

                    votos_candidato = sum(1 for voto in votos_nominais if voto['Cargo'] == cargo and voto['Voto'] == str(numero))

                    percentual = (votos_candidato / total_votos_nominais) * 100 if total_votos_nominais != 0 else 0

                    arquivo.write(
                        f"Candidato: {candidato['nome']} | Cargo: {candidato['cargo_completo']} | Estado: {estado} | Votos: {votos_candidato} ({percentual:.2f}%)\n"
                    )


                total_brancos = len(brancos)
                total_nulos = len(nulos)

                percentual_brancos = (total_brancos / eleitores_aptos) * 100 if eleitores_aptos != 0 else 0
                percentual_nulos = (total_nulos / eleitores_aptos) * 100 if eleitores_aptos != 0 else 0

                arquivo.write(f"\nVotos em Branco: {total_brancos} ({percentual_brancos:.2f}%)\n")
                arquivo.write(f"Votos Nulos: {total_nulos} ({percentual_nulos:.2f}%)\n")

    print("Boletim de urna gerado com sucesso.")


def exibir_resultados_formatados(apuracao_resultados, candidatos_lista):
    """
        Função para exibir os resultados formatados da apuração.

        Parâmetros:
        - apuracao_resultados: Lista de dicionários contendo a apuração dos votos.
        - candidatos_lista: Lista de candidatos.
        """
    if isinstance(apuracao_resultados, list) and len(apuracao_resultados) > 0:
        for apuracao_estado in apuracao_resultados:
            estado = apuracao_estado.get('UF', '')
            votos_estado = apuracao_estado.get('Votos', [])

            if estado:
                eleitores_aptos = len(set(voto.get('UF') for voto in votos_estado))
                print(f"\nApuração dos votos no estado {estado}:\nEleitores Aptos: {eleitores_aptos}")


                votos_nominais = [v for v in votos_estado if v.get('Votos') and v['Votos'] not in ['Branco', 'Nulo']]
                brancos = [v for v in votos_estado if v.get('Votos') and v['Votos'] == 'Branco']
                nulos = [v for v in votos_estado if v.get('Votos') and v['Votos'] == 'Nulo']

                total_votos_nominais = len(votos_nominais)

                print(f"Total de Votos Nominais: {total_votos_nominais}")
                print(f"Brancos: {len(brancos)}")
                print(f"Nulos: {len(nulos)}")

                print("\nResultados:")
                for candidato in candidatos_lista:
                    cargo, numero = candidato['cargo'], candidato['numero']

                    votos_candidato = sum(1 for v in votos_nominais if v['Votos']['Cargo'] == cargo and v['Votos']['Voto'] == str(numero))
                    percentual = (votos_candidato / total_votos_nominais) * 100 if total_votos_nominais != 0 else 0

                    print(
                        f"Candidato: {candidato['nome']} | Cargo: {candidato['cargo_completo']} | Estado: {estado} | Votos: {votos_candidato} ({percentual:.2f}%)"
                    )
    else:
        print("Não há votos apurados. Apure os votos antes de mostrar os resultados.")

def main():
    """
        Função principal que controla o fluxo do programa.
        """
    candidatos_lista = []
    eleitores_lista = []
    votos_apuracao = None
    apuracao_resultados = None

    while True:
        print("\nMenu:")
        print(f"{Fore.GREEN}1 - Ler arquivo de candidatos{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2 - Ler arquivo de eleitores{Style.RESET_ALL}")
        print(f"{Fore.CYAN}3 - Iniciar votação{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}4 - Mostrar resultados{Style.RESET_ALL}")
        print(f"{Fore.RED}5 - Apurar votos{Style.RESET_ALL}")
        print(f"{Fore.WHITE}6 - Fechar programa{Style.RESET_ALL}")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            candidatos_lista = ler_arquivo_candidatos()
        elif opcao == '2':
            eleitores_lista = ler_arquivo_eleitores()
        elif opcao == '3':
            if candidatos_lista and eleitores_lista:
                estado_urna = input("UF onde está localizada a urna: ").upper()
                votos_apuracao = coletar_votos(candidatos_lista, eleitores_lista, estado_urna)
                print("Votação concluída. Resultados ainda não disponíveis.")
            else:
                print("É necessário ler os arquivos de candidatos e eleitores antes de iniciar a votação.")
        elif opcao == '4':
            if votos_apuracao:
                exibir_resultados_formatados(votos_apuracao, candidatos_lista)
            else:
                print("Não há votos apurados. Realize a votação e a apuração antes de mostrar os resultados.")
        elif opcao == '5':
            if votos_apuracao:
                apuracao_resultados = apurar_votos()
                print("Votos apurados:",
                      apuracao_resultados)
                gerar_boletim_urna(apuracao_resultados, candidatos_lista)
                print("Votos apurados com sucesso.")
            else:
                print("Não há votos para apurar. Realize a votação antes de apurar os votos.")
        elif opcao == '6':
            print("Fechando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()