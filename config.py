"""
CS2 Major Pick'Em 模拟器配置文件
包含：参数配置、队伍类定义、胜率矩阵生成等功能
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING, List, Dict
import json
import sys

if TYPE_CHECKING:
    from pathlib import Path

path_teams = "supplement/austin-stage-2/2025_austin_stage_3.json"
path_winrate = "supplement/austin-stage-2/winrate.json"
path_winrate_bo3 = "supplement/austin-stage-2/winrate-bo3.json"


@dataclass(frozen=True)
class Team:
    """
    队伍类，存储队伍的基本信息和评分
    Attributes:
        id: 队伍唯一标识符
        name: 队伍名称
        seed: 种子排名
    """
    id: int
    name: str
    seed: int

    def __str__(self) -> str:
        return str(self.name)

    def __hash__(self) -> int:
        return self.id


@lru_cache(maxsize=None)
def win_probability(a: Team, b: Team, i: bool = False) -> float:
    """
    从预计算的胜率矩阵中获取队伍a战胜队伍b的概率
    
    Args:
        a: 队伍a
        b: 队伍b
        i: 判断是否为BO3
    
    Returns:
        float: 队伍a的胜率 (0-1之间)
    
    Raises:
        KeyError: 如果胜率矩阵中不存在指定队伍的胜率数据
    """
    try:
        if i:
            wm = load_win_matrix("winrate-bo3.json")
        else:
            wm = load_win_matrix("winrate.json")
        return wm[a.name][b.name]
    except KeyError as e:
        raise ValueError(f"胜率矩阵中缺少队伍数据: {str(e)}") from e


def print_win_matrix(win_matrix: Dict[str, Dict[str, float]], teams: List[Team]) -> None:
    """
    打印胜率矩阵
    
    Args:
        win_matrix: 胜率矩阵
        teams: 队伍列表
    """
    print("胜率矩阵（行队名 vs. 列队名 -> 行队名获胜概率）:")
    
    # 固定列宽
    COLUMN_WIDTH = 10  # 每列固定10个字符宽度
    
    # 打印表头
    header = "队伍".center(COLUMN_WIDTH)
    for team in teams:
        # 如果队伍名太长，截断并添加省略号
        team_name = team.name
        if len(team_name) > COLUMN_WIDTH - 2:
            team_name = team_name[:COLUMN_WIDTH-3] + "..."
        header += team_name.center(COLUMN_WIDTH)
    print(header)
    
    # 打印分隔线
    separator = "-" * COLUMN_WIDTH
    for _ in teams:
        separator += "-" * COLUMN_WIDTH
    print(separator)
    
    # 打印每一行
    for team1 in teams:
        # 如果队伍名太长，截断并添加省略号
        team1_name = team1.name
        if len(team1_name) > COLUMN_WIDTH - 2:
            team1_name = team1_name[:COLUMN_WIDTH-3] + "..."
        row = team1_name.center(COLUMN_WIDTH)
        
        for team2 in teams:
            if team1 == team2:
                row += "-".center(COLUMN_WIDTH)
            else:
                win_rate = win_matrix[team1.name][team2.name]
                row += f"{win_rate:.2f}".center(COLUMN_WIDTH)
        print(row)


def load_teams(file_path: str) -> List[Team]:
    """
    从JSON文件加载队伍数据
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        List[Team]: 队伍列表
    
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    """
    with open(file_path) as file:
        data = json.load(file)
    
    teams = []
    for i, (team_name, team_data) in enumerate(data["teams"].items()):
        teams.append(Team(
            id=i,
            name=team_name,
            seed=team_data["seed"]
        ))
    
    return teams


def load_win_matrix(file_path: str) -> Dict[str, Dict[str, float]]:
    """
    从JSON文件加载胜率矩阵数据
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        Dict[str, Dict[str, float]]: 胜率矩阵 {队伍A: {队伍B: A胜B的概率}}
    
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    """
    with open(file_path) as file:
        return json.load(file)


def main():
    """主函数，用于测试配置和函数"""
    try:
        # 加载队伍数据
        teams = load_teams(path_teams)
        # 加载胜率矩阵
        win_matrix = load_win_matrix(path_winrate)
        win_matrix_bo3 = load_win_matrix(path_winrate_bo3)

        # 测试打印胜率矩阵
        print("BO1")
        print_win_matrix(win_matrix, teams)
        print("\nBO3")
        print_win_matrix(win_matrix_bo3, teams)

    except FileNotFoundError:
        print(f"错误：找不到文件")
    except json.JSONDecodeError:
        print(f"错误：不是有效的JSON文件")
    except Exception as e:
        print(f"发生错误：{str(e)}")


if __name__ == "__main__":
    main()
