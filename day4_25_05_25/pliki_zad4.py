import glob

folder_path = "katalog"

txt_files = glob.glob(f"{folder_path} *.txt")
print(f"Znalezione pliki .txt: {txt_files}")

pattern_files = glob.glob(f"{folder_path}file_[0-2].txt")
print(f"Znaleziono pliki wg. wzorca .txt {pattern_files}")

all_txt_recursive = glob.glob("**/*.txt", recursive=True)
print(f" Znaleziono {all_txt_recursive}")