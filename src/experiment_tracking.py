from datetime import datetime
from pathlib import Path
import json
import re
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


PASTA_EXPERIMENTOS = Path("../outputs/experiments")


def normalizar_nome(texto: str) -> str:
    """
    Transforma um nome em um formato seguro para pasta e arquivo.
    """

    texto = texto.strip().lower()
    texto = re.sub(r"[^a-z0-9_-]+", "_", texto)
    texto = re.sub(r"_+", "_", texto)

    return texto.strip("_")


def iniciar_experimento(
    nome_experimento: str,
    pasta_base: Path = PASTA_EXPERIMENTOS
) -> dict[str, Any]:
    """
    Cria uma pasta exclusiva para uma execução do modelo.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_normalizado = normalizar_nome(nome_experimento)

    run_id = f"{timestamp}__{nome_normalizado}"

    pasta_run = pasta_base / run_id
    pasta_plots = pasta_run / "plots"
    pasta_dados_graficos = pasta_run / "dados_graficos"

    pasta_plots.mkdir(parents=True, exist_ok=False)
    pasta_dados_graficos.mkdir(parents=True, exist_ok=False)

    print(f"Experimento criado: {run_id}")
    print(f"Pasta: {pasta_run.resolve()}")

    return {
        "run_id": run_id,
        "nome_experimento": nome_experimento,
        "pasta_run": pasta_run,
        "pasta_plots": pasta_plots,
        "pasta_dados_graficos": pasta_dados_graficos,
        "data_execucao": datetime.now().isoformat(timespec="seconds")
    }

def salvar_figura(
    fig: plt.Figure,
    pasta_plots: Path,
    nome_arquivo: str,
    salvar_pdf: bool = False,
    fechar: bool = False
) -> None:
    """
    Salva uma figura em PNG e, opcionalmente, em PDF.
    """

    nome_normalizado = normalizar_nome(nome_arquivo)

    caminho_png = pasta_plots / f"{nome_normalizado}.png"

    fig.savefig(
        caminho_png,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    if salvar_pdf:
        caminho_pdf = pasta_plots / f"{nome_normalizado}.pdf"

        fig.savefig(
            caminho_pdf,
            bbox_inches="tight",
            facecolor="white"
        )

    if fechar:
        plt.close(fig)

    print(f"Figura salva: {caminho_png}")


def converter_para_json(valor: Any) -> Any:
    """
    Converte tipos do NumPy e pandas para tipos compatíveis com JSON.
    """

    if hasattr(valor, "item"):
        return valor.item()

    if isinstance(valor, Path):
        return str(valor)

    if isinstance(valor, dict):
        return {
            chave: converter_para_json(item)
            for chave, item in valor.items()
        }

    if isinstance(valor, (list, tuple)):
        return [
            converter_para_json(item)
            for item in valor
        ]

    return valor


def salvar_json(
    dados: dict,
    caminho: Path
) -> None:
    """
    Salva um dicionário em um arquivo JSON.
    """

    dados_convertidos = converter_para_json(dados)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados_convertidos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )