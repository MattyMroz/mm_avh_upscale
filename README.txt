start.py - program startowy
clean_frames.py - czyszczenie folderów tymczasowych

./input - tam wkładasz pliki video, audio, obrazy
./input/(inne foldery) - foldery i programy pomocnicze
./output - tam otrzymujesz wyniki działania


Potrzebne do użytkowania:
1. Python: https://www.python.org/downloads/ - przy instalacji zaznacz PATH
	cmd: python --version - czy działa
2. FFmpeg
	Jak pobrać FFmpeg w Windows
	https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z -- auto pobieranie
	Zmienne środowiskowe użytkownika w PATH dodaj -> ścieżkę do folderu: C:\FFmpeg\bin
	cmd: ffmpeg -version -- czy działa
3. Karta graficzna, dobry procesor i RAM
4. vulkan-1.dll - https://www.mediafire.com/file/68o363fbeokdt9w/VulkanRT-Install.zip/file


Real-ESRGAN-ncnn-vulkan GitHub
https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan


Porady:

By wkleić coś w CMD naciśnij prawy przycisk myszy

Pliki ze spacjami piszemy w cudzysłowie "To jest plik.mp4"


SKolowanie:

JPG - domyślnie

def video_to_frames(filename):
    # Ffmpeg pobierze klatki z video i zapisze je w folderze tmp_frames
    cmd('ffmpeg -i ./input/' + filename +
        ' -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 ./tmp_frames/frame%08d.jpg')

def frames_to_video_with_sound(filename, fps):
    # Połączenie ulepszonych klatek z powrotem w video, gdzie dźwięk zostanie skopiowany z pierwotnego video
    cmd('ffmpeg -r ' + fps + ' -i ./out_frames/frame%08d.jpg -i ./input/' + filename + ' -map 0:v:0 -map 1:a:0 -c:a copy -c:v libx264 -r ' +
        fps + ' -pix_fmt yuv420p -crf 10 -preset veryslow -color_primaries bt709 -color_trc bt709 -colorspace bt709 ./output/' + filename)


PNG = 28 razy większy folder tmp_frames - wielkość out_frames jest dotkliwa

def video_to_frames(filename):
    # Ffmpeg pobierze klatki z video i zapisze je w folderze tmp_frames
    cmd('ffmpeg -i ./input/' + filename +
        ' -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 ./tmp_frames/frame%08d.png')

def frames_to_video_with_sound(filename, fps):
    # Połączenie ulepszonych klatek z powrotem w video, gdzie dźwięk zostanie skopiowany z pierwotnego video
    cmd('ffmpeg -r ' + fps + ' -i ./out_frames/frame%08d.png -i ./input/' + filename + ' -map 0:v:0 -map 1:a:0 -c:a copy -c:v libx264 -r ' +
        fps + ' -pix_fmt yuv420p -crf 10 -preset veryslow -color_primaries bt709 -color_trc bt709 -colorspace bt709 ./output/' + filename)


Podsumowanie:
1.
	Funkcja vido_to_frames(), niezależnie od plików output'owych jpg/png, zawsze zapisuje je z lekko przekłamanymi kolorami
2.
	Nie opłaca się używać png, bo pliki w sumie 28 razy większe, a różnica w jakości jest niewielka - choć prawie niweluje to problem z łączeniem pikseli o podobnych kolorach - mniejsze plamy barwne i lepszy gradient
3.
	-crf 0 - 51 odpowiada za jakość obrazu, gdzie 0 to najlepsza jakość, a 51 najgorsza, ale najmniejszy rozmiar pliku, w przypadku scalania klatek z jpg najlepiej wartoiści od 0 - 18 różnią niezauważalnie - ale różnica rozmiaru jest znaczna
4.
	-preset veryslow do ultrafast odpowiada za szybkość kodowania, gdzie ultrafast to najmniejsza jakość, a veryslow największa, ale najmniejszy rozmiar pliku - jakość różnie się niezauważalnie, ale szybkość i rozmiar pliku zmieniają się odpowiednio
5.
	-color_primaries bt709 -color_trc bt709 -colorspace bt709 - zmieniają kolory da identyczne do orginału w jpg, ale w png minimalnie się różnią
6.
	Nie dodając -pix_fmt yuv420p kolory wyjściowe stają się kontrastowe, czarne stają się czarniejsze, a białe wydaje bardziej świecące - fajnie wygląda ten filtr przy walkach, ale może powodować, że kolory będą bardziej przekłamane lub za czarne

Przykłady:

Kompromis jakość - szybkość - rozmiar pliku
	-pix_fmt yuv420p -crf 10 -preset veryslow -color_primaries bt709 -color_trc bt709 -colorspace bt709

Najlepsza jakość
	-pix_fmt yuv420p -crf 0 -preset veryslow -color_primaries bt709 -color_trc bt709 -colorspace bt709

Burżuazja co powyżej ale zamień jpg na png - jeszcze lepsza jakość i większyrozmiar pliku

Wersja budżetowa - mały rozmiar pliku i szybkość
	-pix_fmt yuv420p -crf 18 -preset veryslow -color_primaries bt709 -color_trc bt709 -colorspace bt709

Walki - większy kontrast - nie piszemy -pix_fmt yuv420p

Najlepsza jakosć i szybkość, ale ogromny plik
	-pix_fmt yuv420p -crf 0 -preset ultrafast -color_primaries bt709 -color_trc bt709 -colorspace bt709

