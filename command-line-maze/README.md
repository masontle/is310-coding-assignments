# The Hip-Hop Sample Lineage Maze — Mason Le

This maze is about hip-hop sampling and the way a short piece of recorded sound can connect different artists, genres, and decades. The goal is to trace one sample through the archive until you reach the solution.

## Getting started

1. Unzip `hip-hop-sample-lineage-maze.zip`.
2. Open a terminal or PowerShell window in the unzipped `hip-hop-sample-lineage-maze` folder.
3. Windows PowerShell users should run `.\hide-dotfiles.ps1` before starting so the hidden clue behaves like a hidden file. If PowerShell blocks the script, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\hide-dotfiles.ps1
   ```

4. Begin in the `entrance` directory and read `start-here.txt`.
5. Follow the clues until you find the solution file. Some directories are dead ends, so pay attention to the language in each clue.

## Useful commands

| Task | macOS/Linux | PowerShell |
|---|---|---|
| Show the current location | `pwd` | `Get-Location` |
| List files | `ls` | `Get-ChildItem` |
| Show hidden items | `ls -la` | `Get-ChildItem -Force` |
| Enter a directory | `cd directory-name` | `cd directory-name` |
| Move up one level | `cd ..` | `cd ..` |
| Read a text file | `cat file.txt` | `Get-Content file.txt` |
| Search file contents | `grep -R "word" .` | `Get-ChildItem -Recurse -File | Select-String "word"` |

The directory and file names are part of the maze. You do not need to edit, rename, or delete anything to solve it.
