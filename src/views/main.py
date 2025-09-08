from src.controllers.metadata_controller import analyze_file

if __name__ == "__main__":
    file_path = input("Digite o caminho do arquivo que deseja analisar: ")

    try:
        result = analyze_file(file_path)
        print(f"\n📂 Tipo do arquivo: {result['type']}")
        print("📑 Metadados extraídos:\n")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"❌ Erro ao analisar arquivo: {e}")
