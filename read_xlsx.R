read_xlsx_with_custom_types <- function(file_path, sheet = 1, specific_cols = list()) {
  # 列名を取得
  col_names <- names(read_xlsx(file_path, sheet = sheet, n_max = 0))
  num_cols <- length(col_names)
  
  # "guess"で初期化
  col_types <- rep("guess", num_cols)
  
  # 特定の列の型を上書き
  for (col_idx in names(specific_cols)) {
    col_types[as.numeric(col_idx)] <- specific_cols[[col_idx]]
  }
  
  # データ読み込み
  read_xlsx(file_path, sheet = sheet, col_types = col_types)
}

# 使用例: 2列目を"numeric"、4列目を"text"として読み込む
data <- read_xlsx_with_custom_types(
  file_path,
  sheet = 1,
  specific_cols = list("2" = "numeric", "4" = "text")
)
