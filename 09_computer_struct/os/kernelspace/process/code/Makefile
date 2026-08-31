# ============================================
# 处理器管理 Demo - Makefile
# ============================================

CC       = gcc
CFLAGS   = -Wall -Wextra -g -std=c99
INCLUDES = -I./include

# 目录
SRC_DIR   = src
OBJ_DIR   = obj
BIN_DIR   = bin

# 源文件与目标文件
SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
TARGET = $(BIN_DIR)/process_manager

# 默认目标
all: $(TARGET)
	@echo "===== 编译完成: $(TARGET) ====="

# 链接
$(TARGET): $(OBJS) | $(BIN_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# 编译
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# 创建目录
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# 运行
run: $(TARGET)
	./$(TARGET)

# 清理
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "===== 清理完成 ====="

.PHONY: all run clean
