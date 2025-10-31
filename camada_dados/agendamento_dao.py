from camada_dados.db_config import conectar_banco

def buscar_agendamentos_por_usuario(usuario_id):
    conexao = conectar_banco()
    if not conexao:
        return {"pendentes": [], "concluidos": [], "cancelados": []}

    try:
        cursor = conexao.cursor()
        # Consulta todos os agendamentos do usuário
        cursor.execute("""
            SELECT a.id, q.nome AS quadra, a.data, a.hora_inicio, a.hora_fim, a.status
            FROM agendamento a
            JOIN quadra q ON a.id_quadra = q.id
            WHERE a.id_usuario = %s
            ORDER BY a.data DESC, a.hora_inicio;
        """, (usuario_id,))
        
        resultados = cursor.fetchall()
        agendamentos = {"pendentes": [], "concluidos": [], "cancelados": []}

        for linha in resultados:
            item = {
                "id": linha[0],
                "quadra": linha[1],
                "data": linha[2].strftime("%d/%m/%Y"),
                "hora": f"{linha[3].strftime('%H:%M')} - {linha[4].strftime('%H:%M')}",
                "status": linha[5]
            }

            # Classificação automática por status
            status = linha[5].lower()
            if status in ["pendente", "aguardando", "em análise"]:
                agendamentos["pendentes"].append(item)
            elif status in ["concluido", "finalizado", "realizado"]:
                agendamentos["concluidos"].append(item)
            elif status in ["cancelado", "rejeitado"]:
                agendamentos["cancelados"].append(item)
            else:
                agendamentos["pendentes"].append(item)

        return agendamentos

    except Exception as e:
        print("Erro ao buscar agendamentos:", e)
        return {"pendentes": [], "concluidos": [], "cancelados": []}
    finally:
        cursor.close()
        conexao.close()
