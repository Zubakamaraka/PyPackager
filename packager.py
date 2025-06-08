import subprocess
import os
import shutil
import tempfile


def build_exe(project_path, icon_path=None, output_dir=None):
    result = []
    name = os.path.splitext(os.path.basename(project_path))[0]
    temp_dir = tempfile.mkdtemp()

    try:
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--workpath", os.path.join(temp_dir, "work"),
            "--specpath", temp_dir
        ]

        if icon_path:
            cmd.extend(["--icon", icon_path])

        if output_dir:
            dist_path = os.path.abspath(output_dir)
            cmd.extend(["--distpath", dist_path])
        else:
            dist_path = "dist"

        cmd.append(project_path)

        result.append(f"[BUILD] Команда: {' '.join(cmd)}")
        result.append(f"[BUILD] Временная папка: {temp_dir}")

        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                line = line.strip()
                if line:
                    result.append(line)

            return_code = process.wait()

            if return_code == 0:
                result.append(f"[✓] EXE создан в: {dist_path}")
                result.append(f"[✓] Временные файлы очищены")
            else:
                result.append(f"[!] Процесс завершился с кодом: {return_code}")

        except Exception as e:
            result.append(f"[Ошибка] {str(e)}")

    finally:
        try:
            shutil.rmtree(temp_dir)
            result.append(f"[✓] Временная папка удалена: {temp_dir}")
        except Exception as e:
            result.append(f"[!] Не удалось удалить временную папку: {str(e)}")

    return result
