from dataclasses import dataclass, field
import os
import subprocess
from typing import List, Optional
from utils.constants import console
from utils.execution_timer import execution_timer


@dataclass(slots=True)
class ImageUpscaler:
    input_path: str = "./input"
    output_path: str = "./output"
    scale: int = 4
    tile_size: int = 0
    model_path: str = "models"
    model_name: str = "realesr-animevideov3-x2"
    gpu_id: str = "auto"
    threads: str = "1:2:2"
    tta_mode: bool = False
    output_format: str = "png"
    verbose: bool = False

    def set_config(self, **kwargs: dict) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _get_command(self) -> List[str]:
        executable: str = "realesrgan-ncnn-vulkan.exe" if os.name == "nt" else "realesrgan-ncnn-vulkan"
        command: List[str] = [
            executable,
            "-i", self.input_path,
            "-o", self.output_path,
            "-s", str(self.scale),
            "-t", str(self.tile_size),
            "-m", self.model_path,
            "-n", self.model_name,
            "-g", self.gpu_id,
            "-j", self.threads,
            "-f", self.output_format
        ]
        if self.tta_mode:
            command.append("-x")
        if self.verbose:
            command.append("-v")
        return command

    def upscale_folder(self, input_folder: str, output_folder: str) -> bool:
        self.input_path = input_folder
        self.output_path = output_folder
        command: List[str] = self._get_command()

        try:
            subprocess.run(command, check=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"Błąd podczas upskalowania: {e}", style="red_bold")
            console.print(
                f"Wyjście standardowe: {e.stdout}", style="red_italic")
            console.print(f"Wyjście błędów: {e.stderr}", style="red_italic")
            return False

    def _scan_models(self) -> List[str]:
        models: List[str] = []
        for file in os.listdir(self.model_path):
            if file.endswith(".bin"):
                models.append(file[:-4])
        return models

    def _set_model(self, model_name: str) -> None:
        if model_name in self._scan_models():
            self.model_name = model_name
            console.print(f"Wybrano model: {model_name}", style="green_bold")
        else:
            raise ValueError(f"Model {model_name} nie istnieje.")

    def choose_model(self) -> None:
        models: List[str] = self._scan_models()
        console.print("Dostępne modele:", style="yellow_bold")
        for i, model in enumerate(models, 1):
            console.print(f"{i}. {model}")

        while True:
            try:
                choice: int = int(input("Wybierz numer modelu: ")) - 1
                if 0 <= choice < len(models):
                    self._set_model(models[choice])
                    break
                else:
                    console.print(
                        "Nieprawidłowy numer. Spróbuj ponownie.", style="red_bold")
            except ValueError:
                console.print("Wprowadź poprawny numer.", style="red_bold")


@execution_timer
def main() -> None:
    upscaler: ImageUpscaler = ImageUpscaler()

    # Wybór modelu
    upscaler.choose_model()

    # Konfiguracja
    upscaler.set_config(output_format="png")

    # Upskalowanie folderu z obrazami
    input_folder: str = "./input"
    output_folder: str = "./output"

    success: bool = upscaler.upscale_folder(input_folder, output_folder)
    if success:
        console.print("Obrazy zostały pomyślnie upskalowane! 🎉",
                      style="green_bold")
    else:
        console.print(
            "Wystąpił błąd podczas upskalowania obrazów. 😞", style="red_bold")


if __name__ == "__main__":
    main()
