
from datetime import datetime, timedelta
import re

class PADChatbot:
    def __init__(self):
        self.state = "inicio"
        self.data = {}
        self.historico = []
        self.substate = None
        
    def registrar_historico(self, acao):
        """Registra cada ação no histórico do processo"""
        self.historico.append({
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'acao': acao
        })

    def validar_prazo(self, dias_uteis):
        """Calcula prazo considerando apenas dias úteis"""
        data_atual = datetime.now()
        dias_adicionados = 0
        while dias_adicionados < dias_uteis:
            data_atual += timedelta(days=1)
            if data_atual.weekday() < 5:  # Segunda a sexta
                dias_adicionados += 1
        return data_atual.strftime('%d/%m/%Y')

    def responder(self, entrada):
        entrada_original = entrada.strip()
        entrada = entrada_original.lower()
        
        self.registrar_historico(f"Usuário: {entrada_original}")

        match self.state:

            case "inicio":
                self.state = "menu_principal"
                return """╔════════════════════════════════════════════════════════════╗
║  SISTEMA DE GESTÃO DE PROCESSOS ADMINISTRATIVOS DISCIPLINARES  ║
║                    POLÍCIA MILITAR DE SERGIPE                  ║
╚════════════════════════════════════════════════════════════╝

Bem-vindo ao sistema de apoio à instauração e condução de PAD.

Este sistema irá guiá-lo através de todas as etapas do processo administrativo disciplinar, conforme o Código de Ética e Disciplina dos Militares do Estado de Sergipe (CEDM/SE).

Digite uma das opções:
[1] Instaurar novo PAD
[2] Consultar PAD em andamento
[3] Orientações gerais sobre PAD
[4] Sair

Sua escolha:"""

            case "menu_principal":
                if entrada == "1":
                    self.state = "identificacao_autoridade"
                    return """═══════════════════════════════════════════════
ETAPA 1: IDENTIFICAÇÃO DA AUTORIDADE
═══════════════════════════════════════════════

Antes de iniciar o PAD, preciso confirmar sua identificação.

Informe os seguintes dados:
- Nome completo
- Posto/Graduação
- Função/Cargo (ex: Comandante do 1º BPM)
- Matrícula

Formato: Nome | Posto | Função | Matrícula"""

                elif entrada == "2":
                    return "Funcionalidade em desenvolvimento. Digite [voltar] para retornar."
                
                elif entrada == "3":
                    self.state = "orientacoes"
                    return self.exibir_orientacoes()
                
                elif entrada == "4":
                    return "Sistema encerrado. Até logo!"
                
                else:
                    return "Opção inválida. Digite 1, 2, 3 ou 4."

            case "identificacao_autoridade":
                if self.validar_dados_autoridade(entrada_original):
                    partes = entrada_original.split('|')
                    self.data['autoridade'] = {
                        'nome': partes[0].strip(),
                        'posto': partes[1].strip(),
                        'funcao': partes[2].strip(),
                        'matricula': partes[3].strip()
                    }
                    self.state = "verificacao_competencia"
                    return f"""✓ Dados registrados com sucesso!

Autoridade: {self.data['autoridade']['posto']} {self.data['autoridade']['nome']}
Função: {self.data['autoridade']['funcao']}

═══════════════════════════════════════════════
ETAPA 2: VERIFICAÇÃO DE COMPETÊNCIA
═══════════════════════════════════════════════

Conforme o CEDM/SE, você possui competência para instaurar PAD?

COMPETÊNCIAS:
- Comandantes de OPM
- Comandante-Geral da PMSE
- Autoridades delegadas por ato normativo

Você confirma sua competência para instaurar este PAD? [sim/não]"""
                else:
                    return "❌ Formato inválido. Use: Nome | Posto | Função | Matrícula"

            case "verificacao_competencia":
                if entrada == "sim":
                    self.state = "descricao_fato"
                    return """✓ Competência confirmada.

═══════════════════════════════════════════════
ETAPA 3: DESCRIÇÃO DO FATO MOTIVADOR
═══════════════════════════════════════════════

Descreva detalhadamente o fato que motivou a instauração do PAD.

IMPORTANTE: Seja claro e objetivo. Inclua:
- Data e hora do fato
- Local da ocorrência
- Circunstâncias
- Testemunhas (se houver)
- Documentos relacionados

Digite a descrição completa do fato:"""
                else:
                    self.state = "fim"
                    return """❌ Sem competência para instaurar PAD.

Providências necessárias:
1. Encaminhe a comunicação do fato à autoridade competente
2. Preserve todas as provas e documentos
3. Consulte o setor jurídico para orientações

Sistema encerrado."""

            case "descricao_fato":
                self.data['fato'] = entrada_original
                self.data['data_fato'] = datetime.now().strftime('%d/%m/%Y')
                self.state = "analise_preliminar"
                return f"""✓ Fato registrado com sucesso.

═══════════════════════════════════════════════
ETAPA 4: ANÁLISE PRELIMINAR
═══════════════════════════════════════════════

Analisando o fato descrito:
"{self.data['fato']}"

PERGUNTAS DE ANÁLISE:

1. O fato constitui possível transgressão disciplinar segundo o CEDM/SE? [sim/não]
2. Há elementos suficientes para identificar o(s) militar(es) envolvido(s)? [sim/não]
3. O fato está dentro do prazo prescricional? [sim/não]

Responda no formato: sim/sim/sim ou não/sim/não (conforme cada pergunta)"""

            case "analise_preliminar":
                respostas = entrada.split('/')
                if len(respostas) == 3 and all(r in ['sim', 'não'] for r in respostas):
                    if respostas[0] == 'não':
                        self.state = "fim"
                        return """❌ ANÁLISE: O fato não constitui transgressão disciplinar.

Recomendação: Arquive a comunicação ou trate por outros meios administrativos.
Sistema encerrado."""
                    elif respostas[1] == 'não':
                        self.state = "fim"
                        return """❌ ANÁLISE: Elementos insuficientes para identificação.

Recomendação: Realize sindicância para apuração prévia.
Sistema encerrado."""
                    elif respostas[2] == 'não':
                        self.state = "fim"
                        return """❌ ANÁLISE: Fato prescrito.

A prescrição impede a instauração do PAD.
Sistema encerrado."""
                    else:
                        self.state = "dados_acusado"
                        return """✓ Análise preliminar favorável à instauração do PAD.

═══════════════════════════════════════════════
ETAPA 5: IDENTIFICAÇÃO DO(S) ACUSADO(S)
═══════════════════════════════════════════════

Informe os dados do(s) militar(es) acusado(s):

Para CADA acusado, forneça:
- Nome completo
- RG (registro geral)
- Matrícula
- Posto/Graduação
- OPM de lotação

Formato: Nome | RG | Matrícula | Posto | OPM

Para múltiplos acusados, separe por ponto e vírgula (;)"""
                else:
                    return "❌ Formato inválido. Responda: sim/sim/sim ou não/sim/não"

            case "dados_acusado":
                if self.validar_dados_acusado(entrada_original):
                    acusados = entrada_original.split(';')
                    self.data['acusados'] = []
                    for acusado in acusados:
                        partes = acusado.split('|')
                        self.data['acusados'].append({
                            'nome': partes[0].strip(),
                            'rg': partes[1].strip(),
                            'matricula': partes[2].strip(),
                            'posto': partes[3].strip(),
                            'opm': partes[4].strip()
                        })
                    
                    self.state = "classificacao_transgressao"
                    return f"""✓ {len(self.data['acusados'])} acusado(s) registrado(s).

═══════════════════════════════════════════════
ETAPA 6: CLASSIFICAÇÃO DA TRANSGRESSÃO
═══════════════════════════════════════════════

Classifique a gravidade da transgressão conforme o CEDM/SE:

[1] Leve - Passível de advertência ou repreensão
[2] Média - Passível de suspensão ou detenção
[3] Grave - Passível de demissão ou expulsão

Digite o número da classificação:"""
                else:
                    return "❌ Formato inválido. Use: Nome | RG | Matrícula | Posto | OPM"

            case "classificacao_transgressao":
                classificacoes = {
                    '1': 'Leve',
                    '2': 'Média',
                    '3': 'Grave'
                }
                if entrada in classificacoes:
                    self.data['classificacao'] = classificacoes[entrada]
                    self.state = "designacao_comissao"
                    return f"""✓ Transgressão classificada como: {self.data['classificacao']}

═══════════════════════════════════════════════
ETAPA 7: DESIGNAÇÃO DA COMISSÃO PROCESSANTE
═══════════════════════════════════════════════

A comissão deve ser composta por 3 (três) oficiais:
- 1 Presidente (oficial superior, preferencialmente)
- 2 Membros (sendo um deles o Secretário)

REQUISITOS:
✓ Posto/graduação igual ou superior ao acusado
✓ Não possuir parentesco com o acusado
✓ Não ter interesse direto no processo
✓ Estar no efetivo serviço

Informe os dados da comissão:

Para CADA membro, forneça:
- Nome completo
- Posto/Graduação
- Matrícula
- Função na comissão (Presidente/Membro/Secretário)

Formato: Nome | Posto | Matrícula | Função

Separe os membros por ponto e vírgula (;)"""
                else:
                    return "❌ Opção inválida. Digite 1, 2 ou 3."

            case "designacao_comissao":
                if self.validar_dados_comissao(entrada_original):
                    membros = entrada_original.split(';')
                    self.data['comissao'] = []
                    for membro in membros:
                        partes = membro.split('|')
                        self.data['comissao'].append({
                            'nome': partes[0].strip(),
                            'posto': partes[1].strip(),
                            'matricula': partes[2].strip(),
                            'funcao': partes[3].strip()
                        })
                    
                    if len(self.data['comissao']) != 3:
                        return "❌ A comissão deve ter exatamente 3 membros. Tente novamente."
                    
                    funcoes = [m['funcao'].lower() for m in self.data['comissao']]
                    if 'presidente' not in funcoes or 'secretário' not in funcoes:
                        return "❌ É necessário designar 1 Presidente e 1 Secretário. Tente novamente."
                    
                    self.state = "prazo_conclusao"
                    return """✓ Comissão designada com sucesso!

═══════════════════════════════════════════════
ETAPA 8: DEFINIÇÃO DE PRAZO
═══════════════════════════════════════════════

Conforme o CEDM/SE, o PAD deve ser concluído em:
Art. 80. O prazo para conclusão do Processo Administrativo Disciplinar será de 15 (quinze) dias úteis.
§ 1º Este prazo poderá ser prorrogado por mais 05 (cinco) dias úteis, desde que fundamentadamente justificado, e em tempo oportuno, de modo a ser atendido antes do término do prazo definido no caput deste artigo.

Informe o prazo desejado em dias úteis (ex: 60):"""
                else:
                    return "❌ Formato inválido. Use: Nome | Posto | Matrícula | Função"

            case "prazo_conclusao":
                if entrada.isdigit():
                    prazo = int(entrada)
                    if prazo > 0 and prazo <= 180:
                        self.data['prazo_dias'] = prazo
                        self.data['prazo_final'] = self.validar_prazo(prazo)
                        self.state = "gerar_portaria"
                        return f"""✓ Prazo definido: {prazo} dias úteis
  Data limite: {self.data['prazo_final']}

═══════════════════════════════════════════════
ETAPA 9: GERAÇÃO DA PORTARIA DE INSTAURAÇÃO
═══════════════════════════════════════════════

Todos os dados foram coletados. Deseja gerar a Portaria de Instauração do PAD?

[sim] - Gerar portaria
[revisar] - Revisar dados antes de gerar
[cancelar] - Cancelar processo"""
                else:
                    return "❌ Digite um número válido de dias (1 a 180)."

            case "gerar_portaria":
                if entrada == "sim":
                    self.state = "portaria_gerada"
                    return self.gerar_portaria_instauracao()
                elif entrada == "revisar":
                    return self.exibir_resumo_dados() + "\n\nDigite [continuar] para gerar a portaria ou [editar] para alterar algum dado."
                elif entrada == "cancelar":
                    self.state = "fim"
                    return "Processo cancelado. Sistema encerrado."
                else:
                    return "❌ Opção inválida. Digite: sim, revisar ou cancelar"

            case "portaria_gerada":
                self.state = "termo_citacao"
                return """
A portaria foi gerada com sucesso!

═══════════════════════════════════════════════
ETAPA 10: CITAÇÃO DO(S) ACUSADO(S)
═══════════════════════════════════════════════

ATENÇÃO: A citação é ato essencial do PAD!

O acusado deve ser citado PESSOALMENTE para:
✓ Tomar conhecimento da acusação
✓ Ter acesso aos autos do processo
✓ Apresentar defesa prévia (5 dias úteis)

Deseja gerar o Termo de Citação? [sim/não]"""

            case "termo_citacao":
                if entrada == "sim":
                    self.state = "acompanhamento_citacao"
                    return self.gerar_termo_citacao()
                else:
                    return "A citação deve ser realizada. Digite [sim] quando estiver pronto."

            case "acompanhamento_citacao":
                if entrada in ["sim", "concluída", "citado"]:
                    self.data['data_citacao'] = datetime.now().strftime('%d/%m/%Y')
                    self.data['prazo_defesa'] = self.validar_prazo(5)
                    self.state = "aguardando_defesa"
                    return f"""✓ Citação registrada em: {self.data['data_citacao']}

═══════════════════════════════════════════════
ETAPA 11: DEFESA PRÉVIA
═══════════════════════════════════════════════

O acusado tem até {self.data['prazo_defesa']} para apresentar defesa prévia.

Opções:
[1] Acusado apresentou defesa prévia
[2] Acusado não apresentou defesa (revelia)
[3] Aguardando prazo

Digite a opção:"""
                else:
                    return "Confirme a realização da citação digitando: sim, concluída ou citado"

            case "aguardando_defesa":
                if entrada == "1":
                    self.state = "instrucao_processual"
                    return """✓ Defesa prévia recebida e juntada aos autos.

═══════════════════════════════════════════════
ETAPA 12: INSTRUÇÃO PROCESSUAL
═══════════════════════════════════════════════

Nesta fase, a comissão deve:
✓ Ouvir testemunhas
✓ Realizar diligências
✓ Juntar documentos
✓ Interrogar o acusado
✓ Produzir demais provas necessárias

Digite [iniciar] quando a instrução estiver concluída:"""
                
                elif entrada == "2":
                    self.data['defesa_previa'] = "Revelia - acusado não apresentou defesa no prazo legal"
                    self.state = "instrucao_processual"
                    return """✓ Revelia registrada. O processo prossegue sem a defesa prévia.

═══════════════════════════════════════════════
ETAPA 12: INSTRUÇÃO PROCESSUAL
═══════════════════════════════════════════════

Nesta fase, a comissão deve:
✓ Ouvir testemunhas
✓ Realizar diligências
✓ Juntar documentos
✓ Interrogar o acusado
✓ Produzir demais provas necessárias

Digite [iniciar] quando a instrução estiver concluída:"""
                
                elif entrada == "3":
                    return f"Prazo para defesa prévia: até {self.data['prazo_defesa']}. Digite [1] ou [2] quando o prazo expirar."
                
                else:
                    return "❌ Opção inválida. Digite 1, 2 ou 3."

            case "instrucao_processual":
                if entrada == "iniciar":
                    self.state = "coleta_provas"
                    return """═══════════════════════════════════════════════
REGISTRO DE PROVAS E DILIGÊNCIAS
═══════════════════════════════════════════════

Registre as principais provas e diligências realizadas:

Formato sugerido:
- Testemunha 1: [nome e síntese do depoimento]
- Testemunha 2: [nome e síntese do depoimento]
- Documentos: [lista de documentos juntados]
- Perícias: [se houver]
- Outras diligências: [descrever]

Digite o resumo da instrução:"""
                else:
                    return "Digite [iniciar] quando a fase instrutória estiver concluída."

            case "coleta_provas":
                self.data['provas'] = entrada_original
                self.state = "interrogatorio"
                return """✓ Provas registradas.

═══════════════════════════════════════════════
ETAPA 13: INTERROGATÓRIO DO ACUSADO
═══════════════════════════════════════════════

O interrogatório é o último ato da instrução.

O acusado foi interrogado? [sim/não]"""

            case "interrogatorio":
                if entrada == "sim":
                    self.state = "alegacoes_finais"
                    return """✓ Interrogatório realizado.

═══════════════════════════════════════════════
ETAPA 14: ALEGAÇÕES FINAIS
═══════════════════════════════════════════════

Após a instrução, o acusado tem direito a apresentar alegações finais.

Prazo: 5 dias úteis

O acusado apresentou alegações finais? [sim/não/não quis]"""
                else:
                    return "O interrogatório é obrigatório. Digite [sim] quando for realizado."

            case "alegacoes_finais":
                if entrada in ["sim", "não", "não quis"]:
                    self.data['alegacoes_finais'] = entrada
                    self.state = "relatorio_comissao"
                    return """✓ Fase instrutória encerrada.

═══════════════════════════════════════════════
ETAPA 15: RELATÓRIO FINAL DA COMISSÃO
═══════════════════════════════════════════════

A comissão deve elaborar relatório conclusivo indicando:
✓ Síntese dos fatos
✓ Provas produzidas
✓ Análise da conduta
✓ Conclusão (absolvição ou responsabilização)
✓ Sanção sugerida (se houver)

Deseja gerar o modelo de Relatório Final? [sim]"""
                else:
                    return "Digite: sim, não ou não quis"

            case "relatorio_comissao":
                if entrada == "sim":
                    self.state = "decisao_autoridade"
                    return self.gerar_relatorio_comissao()
                else:
                    return "Digite [sim] para gerar o relatório."

            case "decisao_autoridade":
                return """
═══════════════════════════════════════════════
ETAPA 16: DECISÃO DA AUTORIDADE COMPETENTE
═══════════════════════════════════════════════

A autoridade deve:
✓ Analisar o relatório da comissão
✓ Verificar a legalidade do processo
✓ Decidir pela absolvição ou aplicação de sanção

Decisão:
[1] Acolher integralmente o relatório
[2] Acolher parcialmente o relatório
[3] Rejeitar o relatório (determinar novas diligências)
[4] Absolver por falta de provas

Digite a opção:"""

            case "despacho_decisorio":
                opcoes_decisao = {
                    '1': 'acolhimento integral',
                    '2': 'acolhimento parcial',
                    '3': 'rejeição com novas diligências',
                    '4': 'absolvição'
                }
                if entrada in opcoes_decisao:
                    self.data['tipo_decisao'] = opcoes_decisao[entrada]
                    self.state = "fim"
                    return self.gerar_despacho_decisorio()
                else:
                    return "❌ Opção inválida. Digite 1, 2, 3 ou 4."

            case "orientacoes":
                if entrada == "voltar":
                    self.state = "menu_principal"
                    return "Digite [1] para instaurar novo PAD."
                else:
                    return self.exibir_orientacoes()

            case "fim":
                return """
╔════════════════════════════════════════════╗
║           PAD FINALIZADO COM SUCESSO        ║
╚════════════════════════════════════════════╝

Todos os documentos foram gerados.

PRÓXIMAS PROVIDÊNCIAS:
✓ Arquivar todos os documentos nos autos
✓ Publicar a decisão em Boletim
✓ Comunicar ao acusado
✓ Registrar no sistema de gestão de pessoal

Para iniciar novo PAD, reinicie o sistema.
"""

            case _:
                return "❌ Estado desconhecido. Digite [reiniciar] para começar novamente."

    def validar_dados_autoridade(self, entrada):
        """Valida formato dos dados da autoridade"""
        partes = entrada.split('|')
        return len(partes) == 4 and all(p.strip() for p in partes)

    def validar_dados_acusado(self, entrada):
        """Valida formato dos dados do acusado"""
        acusados = entrada.split(';')
        for acusado in acusados:
            partes = acusado.split('|')
            if len(partes) != 5 or not all(p.strip() for p in partes):
                return False
        return True

    def validar_dados_comissao(self, entrada):
        """Valida formato dos dados da comissão"""
        membros = entrada.split(';')
        for membro in membros:
            partes = membro.split('|')
            if len(partes) != 4 or not all(p.strip() for p in partes):
                return False
        return True

    def exibir_resumo_dados(self):
        """Exibe resumo de todos os dados coletados"""
        resumo = "\n═══════════════════════════════════════════════\n"
        resumo += "RESUMO DOS DADOS COLETADOS\n"
        resumo += "═══════════════════════════════════════════════\n\n"
        
        resumo += f"AUTORIDADE INSTAURADORA:\n"
        resumo += f"  {self.data['autoridade']['posto']} {self.data['autoridade']['nome']}\n"
        resumo += f"  Função: {self.data['autoridade']['funcao']}\n\n"
        
        resumo += f"FATO MOTIVADOR:\n"
        resumo += f"  {self.data['fato'][:200]}...\n\n"
        
        resumo += f"ACUSADO(S):\n"
        for i, acusado in enumerate(self.data['acusados'], 1):
            resumo += f"  {i}. {acusado['posto']} {acusado['nome']} - RG {acusado['rg']}\n"
        
        resumo += f"\nCOMISSÃO PROCESSANTE:\n"
        for membro in self.data['comissao']:
            resumo += f"  • {membro['funcao']}: {membro['posto']} {membro['nome']}\n"
        
        resumo += f"\nPRAZO: {self.data['prazo_dias']} dias úteis (até {self.data['prazo_final']})\n"
        resumo += f"CLASSIFICAÇÃO: Transgressão {self.data['classificacao']}\n"
        
        return resumo

    def exibir_orientacoes(self):
        """Exibe orientações gerais sobre PAD"""
        return """
═══════════════════════════════════════════════
ORIENTAÇÕES GERAIS SOBRE PAD
═══════════════════════════════════════════════

1. CONCEITO
   O PAD é o instrumento destinado a apurar responsabilidade
   de militar por infração às normas disciplinares.

2. PRINCÍPIOS FUNDAMENTAIS
   ✓ Legalidade
   ✓ Ampla defesa e contraditório
   ✓ Verdade material
   ✓ Oficialidade
   ✓ Celeridade

3. FASES DO PAD
   a) Instauração (portaria)
   b) Citação do acusado
   c) Defesa prévia (5 dias)
   d) Instrução processual
   e) Interrogatório
   f) Alegações finais (5 dias)
   g) Relatório da comissão
   h) Decisão da autoridade

4. PRAZOS
   • Defesa prévia: 5 dias úteis
   • Alegações finais: 5 dias úteis
   • Conclusão do PAD: 60 a 90 dias (prorrogável)

5. GARANTIAS DO ACUSADO
   ✓ Conhecer a acusação
   ✓ Ter acesso aos autos
   ✓ Apresentar defesa
   ✓ Produzir provas
   ✓ Ser interrogado
   ✓ Ter defensor constituído

Digite [voltar] para retornar ao menu principal.
"""

    def gerar_portaria_instauracao(self):
        """Gera a portaria de instauração do PAD"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        portaria = f"""
╔════════════════════════════════════════════════════════════╗
║           PORTARIA DE INSTAURAÇÃO DE PAD N.º ____/____      ║
╚════════════════════════════════════════════════════════════╝

O(A) {self.data['autoridade']['posto']} {self.data['autoridade']['nome']}, 
{self.data['autoridade']['funcao']}, no uso de suas atribuições legais e 
tendo em vista o disposto no Código de Ética e Disciplina dos Militares 
do Estado de Sergipe (CEDM/SE),

RESOLVE:

Art. 1º INSTAURAR Processo Administrativo Disciplinar (PAD) para apurar 
os fatos a seguir descritos:

FATO MOTIVADOR:
{self.data['fato']}

Data do fato: {self.data['data_fato']}
Classificação: Transgressão {self.data['classificacao']}

Art. 2º INDICAR como acusado(s):
"""
        for i, acusado in enumerate(self.data['acusados'], 1):
            portaria += f"""
{i}. {acusado['posto']} {acusado['nome']}
   RG: {acusado['rg']} | Matrícula: {acusado['matricula']}
   OPM: {acusado['opm']}
"""

        portaria += f"""
Art. 3º DESIGNAR para compor a Comissão Processante os seguintes oficiais:
"""
        for membro in self.data['comissao']:
            portaria += f"""
- {membro['funcao'].upper()}: {membro['posto']} {membro['nome']}
  Matrícula: {membro['matricula']}
"""

        portaria += f"""
Art. 4º FIXAR o prazo de {self.data['prazo_dias']} ({"sessenta" if self.data['prazo_dias'] == 60 else "noventa"}) 
dias úteis para conclusão dos trabalhos, contados da data de publicação 
desta Portaria, podendo ser prorrogado por igual período mediante 
justificativa fundamentada.

Art. 5º DETERMINAR que a Comissão Processante observe rigorosamente:
I - Os prazos legais estabelecidos;
II - O direito de ampla defesa e contraditório;
III - O princípio da verdade material;
IV - As normas do CEDM/SE e legislação correlata.

Art. 6º Esta Portaria entra em vigor na data de sua publicação.

PUBLIQUE-SE E CUMPRA-SE.

{self.data['autoridade']['funcao']}, em {hoje}.


_________________________________________
{self.data['autoridade']['posto']} {self.data['autoridade']['nome']}
{self.data['autoridade']['funcao']}
Mat.: {self.data['autoridade']['matricula']}

═══════════════════════════════════════════════

A portaria foi gerada com sucesso!

PRÓXIMO PASSO: A comissão deve ser notificada e o acusado citado.

Digite [continuar] para prosseguir.
"""
        return portaria

    def gerar_termo_citacao(self):
        """Gera o termo de citação do acusado"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        prazo_defesa = self.validar_prazo(5)
        
        termo = f"""
╔════════════════════════════════════════════════════════════╗
║                    TERMO DE CITAÇÃO                         ║
╚════════════════════════════════════════════════════════════╝

Aos {hoje}, nesta cidade de Aracaju/SE, na sede da {self.data['autoridade']['funcao']}, 
foi citado(a) pessoalmente o(a):
"""
        for acusado in self.data['acusados']:
            termo += f"""
{acusado['posto']} {acusado['nome']}
RG: {acusado['rg']} | Matrícula: {acusado['matricula']}
OPM: {acusado['opm']}
"""

        termo += f"""
Para tomar conhecimento da instauração do Processo Administrativo Disciplinar 
(PAD) n.º ____/____, conforme Portaria de Instauração, e apresentar DEFESA 
PRÉVIA no prazo de 5 (cinco) dias úteis, contados a partir desta citação, 
conforme determina o artigo 83 do CEDM/SE.

PRAZO FINAL PARA DEFESA PRÉVIA: {prazo_defesa}

DIREITOS ASSEGURADOS:
✓ Vista integral dos autos do processo
✓ Apresentação de defesa escrita
✓ Juntada de documentos
✓ Arrolamento de testemunhas
✓ Constituição de defensor
✓ Acompanhamento de todos os atos processuais

ADVERTÊNCIAS LEGAIS:
⚠ A não apresentação de defesa no prazo implicará prosseguimento do 
  processo em revelia.
⚠ O acusado tem direito a defensor constituído ou será indicado 
  defensor dativo.
⚠ Todas as comunicações processuais serão realizadas pessoalmente 
  ou mediante publicação em Boletim.

LOCAL PARA VISTA DOS AUTOS:
[Endereço da comissão processante]

HORÁRIO DE ATENDIMENTO:
[Informar horário]

CIENTE:

Local e data: ________________, ___/___/______

_________________________________________
Assinatura do citado

_________________________________________
Testemunha 1

_________________________________________
Testemunha 2

_________________________________________
Membro da Comissão Processante
{self.data['comissao'][0]['posto']} {self.data['comissao'][0]['nome']}

═══════════════════════════════════════════════

IMPORTANTE: Faça 2 vias deste termo:
- 1ª via: Acusado
- 2ª via: Autos do processo

A citação foi realizada? [sim/não]
"""
        return termo

    def gerar_relatorio_comissao(self):
        """Gera o relatório final da comissão"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        relatorio = f"""
╔════════════════════════════════════════════════════════════╗
║              RELATÓRIO FINAL DA COMISSÃO PROCESSANTE        ║
╚════════════════════════════════════════════════════════════╝

PAD N.º ____/____
Data: {hoje}

I - IDENTIFICAÇÃO

Autoridade Instauradora:
{self.data['autoridade']['posto']} {self.data['autoridade']['nome']}
{self.data['autoridade']['funcao']}

Comissão Processante:
"""
        for membro in self.data['comissao']:
            relatorio += f"• {membro['funcao']}: {membro['posto']} {membro['nome']}\n"

        relatorio += f"""
Acusado(s):
"""
        for acusado in self.data['acusados']:
            relatorio += f"• {acusado['posto']} {acusado['nome']} - RG {acusado['rg']}\n"

        relatorio += f"""
II - RESUMO DOS FATOS

{self.data['fato']}

Data do fato: {self.data['data_fato']}
Classificação: Transgressão {self.data['classificacao']}

III - HISTÓRICO PROCESSUAL

- Portaria de Instauração: [data]
- Citação do acusado: {self.data.get('data_citacao', '[data]')}
- Defesa prévia: {"Apresentada" if self.data.get('alegacoes_finais') == 'sim' else "Não apresentada - Revelia"}
- Instrução processual: Realizada conforme termo específico
- Interrogatório: Realizado
- Alegações finais: {self.data.get('alegacoes_finais', '[informar]')}

IV - PROVAS PRODUZIDAS

{self.data.get('provas', '[Descrever provas e diligências realizadas]')}

V - ANÁLISE TÉCNICO-JURÍDICA

[A comissão deve analisar:]

5.1. DOS FATOS APURADOS
[Descrição detalhada dos fatos comprovados durante a instrução]

5.2. DO ENQUADRAMENTO LEGAL
[Indicar o artigo do CEDM/SE que tipifica a conduta]

5.3. DA AUTORIA E MATERIALIDADE
[Demonstrar a prova da autoria e da materialidade da transgressão]

5.4. DAS CIRCUNSTÂNCIAS AGRAVANTES E ATENUANTES
[Analisar as circunstâncias do art. [X] do CEDM/SE]

5.5. DA CONDUTA ANTERIOR DO ACUSADO
[Verificar antecedentes disciplinares]

VI - CONCLUSÃO

Após análise detalhada dos autos, exame de todas as provas produzidas 
e considerando os princípios da legalidade, impessoalidade e moralidade, 
esta Comissão Processante conclui que:

[OPÇÃO 1 - SE PROCEDENTE:]
O acusado {self.data['acusados'][0]['posto']} {self.data['acusados'][0]['nome']} 
praticou a transgressão disciplinar descrita nos autos, conforme tipificação 
do art. [X] do CEDM/SE.

[OPÇÃO 2 - SE IMPROCEDENTE:]
Não restou comprovada a prática de transgressão disciplinar pelo acusado, 
devendo ser absolvido por falta de provas.

VII - SUGESTÃO DE SANÇÃO (se procedente)

Com base no art. [X] do CEDM/SE e considerando:
- Gravidade da transgressão: {self.data['classificacao']}
- Circunstâncias do fato
- Antecedentes do acusado
- Dano causado ao serviço

Esta comissão sugere a aplicação da seguinte sanção:
[Indicar: Advertência / Repreensão / Suspensão / Detenção / Demissão / Expulsão]

Período: [se aplicável]
Fundamentação: [justificar a proporcionalidade]

VIII - ENCERRAMENTO

São estes os termos do presente Relatório Final, que submetemos à 
elevada apreciação de Vossa Senhoria para decisão.

Aracaju/SE, {hoje}.


_________________________________________
{self.data['comissao'][0]['posto']} {self.data['comissao'][0]['nome']}
Presidente da Comissão

_________________________________________
{self.data['comissao'][1]['posto']} {self.data['comissao'][1]['nome']}
Membro da Comissão

_________________________________________
{self.data['comissao'][2]['posto']} {self.data['comissao'][2]['nome']}
Secretário da Comissão

═══════════════════════════════════════════════

Relatório gerado com sucesso!

ATENÇÃO: Complete os campos indicados entre colchetes [X] com as 
informações específicas do caso.

Digite [continuar] para prosseguir para o despacho decisório.
"""
        self.state = "despacho_decisorio"
        return relatorio

    def gerar_despacho_decisorio(self):
        """Gera o despacho decisório da autoridade"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        despacho = f"""
╔════════════════════════════════════════════════════════════╗
║              DESPACHO DECISÓRIO                             ║
╚════════════════════════════════════════════════════════════╝

PAD N.º ____/____
Data: {hoje}

O(A) {self.data['autoridade']['posto']} {self.data['autoridade']['nome']},
{self.data['autoridade']['funcao']}, no uso de suas atribuições legais,

CONSIDERANDO o Relatório Final da Comissão Processante;
CONSIDERANDO as provas constantes dos autos;
CONSIDERANDO a garantia do devido processo legal, ampla defesa e contraditório;
CONSIDERANDO o disposto no CEDM/SE;

DECIDE:
"""

        if self.data['tipo_decisao'] == 'absolvição':
            despacho += f"""
I - ABSOLVER o acusado {self.data['acusados'][0]['posto']} {self.data['acusados'][0]['nome']}, 
RG {self.data['acusados'][0]['rg']}, por falta de provas suficientes para 
sua responsabilização disciplinar.

II - DETERMINAR o arquivamento do presente PAD.

III - DETERMINAR a comunicação ao acusado.
"""
        
        elif self.data['tipo_decisao'] == 'acolhimento integral':
            despacho += f"""
I - ACOLHER INTEGRALMENTE o Relatório Final da Comissão Processante.

II - JULGAR PROCEDENTE a acusação contra o militar 
{self.data['acusados'][0]['posto']} {self.data['acusados'][0]['nome']}, 
RG {self.data['acusados'][0]['rg']}, pela prática de transgressão disciplinar 
tipificada no art. [X] do CEDM/SE.

III - APLICAR a sanção de [INDICAR SANÇÃO] pelo período de [X] dias, 
conforme art. [Y] do CEDM/SE.

IV - DETERMINAR:
a) A publicação desta decisão em Boletim;
b) A comunicação ao acusado para cumprimento da sanção;
c) O registro nos assentamentos funcionais;
d) O arquivamento dos autos.
"""

        elif self.data['tipo_decisao'] == 'acolhimento parcial':
            despacho += f"""
I - ACOLHER PARCIALMENTE o Relatório Final da Comissão Processante.

II - JULGAR PROCEDENTE a acusação, porém com algumas modificações quanto 
à [tipificação / sanção sugerida / fundamentação].

III - APLICAR a sanção de [INDICAR SANÇÃO DIFERENTE DA SUGERIDA], 
fundamentada em [JUSTIFICAR].

IV - DETERMINAR as providências de comunicação, publicação e registro.
"""

        else:  # rejeição com novas diligências
            despacho += f"""
I - DETERMINAR o retorno dos autos à Comissão Processante para realização 
de novas diligências, tendo em vista [FUNDAMENTAR A NECESSIDADE].

II - FIXAR o prazo de [X] dias úteis para conclusão das diligências.

III - DETERMINAR que após as novas diligências, seja elaborado relatório 
complementar.
"""

        despacho += f"""

FUNDAMENTAÇÃO:
[A autoridade deve fundamentar sua decisão com base nos autos, 
nas provas produzidas e na legislação aplicável]

Aracaju/SE, {hoje}.


_________________________________________
{self.data['autoridade']['posto']} {self.data['autoridade']['nome']}
{self.data['autoridade']['funcao']}
Mat.: {self.data['autoridade']['matricula']}

═══════════════════════════════════════════════
═══════════════════════════════════════════════

✓ DESPACHO DECISÓRIO GERADO COM SUCESSO!

PROVIDÊNCIAS FINAIS:
1. Publicar em Boletim
2. Comunicar ao acusado
3. Registrar nos assentamentos
4. Arquivar os autos do processo
5. Dar ciência ao Ministério Público (se aplicável)

═══════════════════════════════════════════════

DOCUMENTOS GERADOS NESTE PAD:
✓ Portaria de Instauração
✓ Termo de Citação
✓ Relatório Final da Comissão
✓ Despacho Decisório

Processo concluído com sucesso!

Para iniciar novo PAD, reinicie o sistema.
"""
        return despacho


# ═══════════════════════════════════════════════
# EXECUÇÃO INTERATIVA DO CHATBOT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SISTEMA DE GESTÃO DE PAD - POLÍCIA MILITAR/SE          ║")
    print("║                    Versão 2.0 - 2025                        ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    chatbot = PADChatbot()
    print("Chatbot:", chatbot.responder(""))
    
    while True:
        try:
            entrada = input("\n>>> Você: ").strip()
            
            if not entrada:
                print("⚠ Digite algo para continuar.")
                continue
            
            if entrada.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Sistema encerrado. Até logo!")
                break
            
            if entrada.lower() == 'reiniciar':
                chatbot = PADChatbot()
                print("\n🔄 Sistema reiniciado.")
                print("Chatbot:", chatbot.responder(""))
                continue
            
            resposta = chatbot.responder(entrada)
            print("\nChatbot:", resposta)
            
            if chatbot.state == "fim":
                reiniciar = input("\nDeseja processar um novo PAD? [sim/não]: ").strip().lower()
                if reiniciar == "sim":
                    chatbot = PADChatbot()
                    print("\n🔄 Sistema reiniciado para novo PAD.")
                    print("Chatbot:", chatbot.responder(""))
                else:
                    print("\n👋 Sistema encerrado. Até logo!")
                    break
        
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupção detectada.")
            salvar = input("Deseja salvar o progresso antes de sair? [sim/não]: ").strip().lower()
            if salvar == "sim":
                print("💾 Funcionalidade de salvamento em desenvolvimento.")
            print("👋 Sistema encerrado.")
            break
        
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            print("Digite [reiniciar] para começar novamente ou [sair] para encerrar.")