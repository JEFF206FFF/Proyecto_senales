import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.fft import rfft, rfftfreq

# Cargar audio de referencia (Target)
fs, target = read('audios/originales/target.wav')
target = target.astype(float) / (2**31)

print("| Mensaje secreto | SNR (dB) | Correlación de Pearson |")
print("| :--- | :---: | :---: |")

for i in range(1, 6):
    # Cargar original x[n] y recuperado x_hat[n] en la misma escala
    _, x = read(f'audios/originales/secret{i}.wav')
    x = x.astype(float) / (2**31)
    
    _, x_hat = read(f'audios/recovered/recovered_{i}.wav')
    x_hat = x_hat.astype(float)
    
    # 1. Cálculo explícito de SNR (dB)
    numerador_snr = np.sum(x**2)
    denominador_snr = np.sum((x - x_hat)**2)
    snr = 10 * np.log10(numerador_snr / denominador_snr)
    
    # 2. Cálculo explícito de Correlación de Pearson
    x_prom = np.mean(x)
    x_hat_prom = np.mean(x_hat)
    
    numerador_p = np.sum((x - x_prom) * (x_hat - x_hat_prom))
    denominador_p = np.sqrt(np.sum((x - x_prom)**2)) * np.sqrt(np.sum((x_hat - x_hat_prom)**2))
    pearson = numerador_p / denominador_p
    
    print(f"| Secret {i} | {snr:.2f} | {pearson:.12f} |")
    
    # Generar las 4 gráficas requeridas usando Secret 1 como ejemplo
    if i == 1:
        _, enc = read('audios/encoded/encoded_1.wav')
        enc = enc.astype(float)
        
        N = len(target)
        t = np.arange(N) / fs
        f = rfftfreq(N, 1/fs)
        
        T_mag = np.abs(rfft(target))
        S_mag = np.abs(rfft(x))
        E_mag = np.abs(rfft(enc))
        
        # Gráfica 1: Dominio temporal (Target vs Secret)
        plt.figure(figsize=(10, 4))
        plt.subplot(2, 1, 1)
        plt.plot(t, target)
        plt.title('Target - Dominio temporal')
        plt.ylabel('Amplitud')
        plt.subplot(2, 1, 2)
        plt.plot(t, x)
        plt.title('Secret 1 - Dominio temporal')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.tight_layout()
        plt.savefig('Grafica_tiempo.png')
        plt.close()
        
        # Gráfica 2: Espectros de magnitud (Target vs Secret)
        plt.figure(figsize=(10, 4))
        plt.subplot(2, 1, 1)
        plt.plot(f, T_mag)
        plt.title('Espectro de magnitud - Target')
        plt.ylabel('Magnitud')
        plt.subplot(2, 1, 2)
        plt.plot(f, S_mag)
        plt.title('Espectro de magnitud - Secret 1')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud')
        plt.tight_layout()
        plt.savefig('Grafica_espectro.png')
        plt.close()
        
        # Gráfica 3: Target vs Secret vs Secret reordenado (3 paneles)
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.plot(f, T_mag)
        plt.title('Target')
        plt.ylabel('Magnitud')
        plt.subplot(3, 1, 2)
        plt.plot(f, S_mag)
        plt.title('Secret')
        plt.ylabel('Magnitud')
        plt.subplot(3, 1, 3)
        plt.plot(f, E_mag)
        plt.title('Secret - Coeficientes reordenados')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud')
        plt.tight_layout()
        plt.savefig('Grafica_espectro_ordenado.png')
        plt.close()
        
        # Gráfica 4: Señal codificada en el dominio temporal
        plt.figure(figsize=(10, 2.5))
        plt.plot(t, enc)
        plt.title('Señal codificada (Encoded 1) - Dominio temporal')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.tight_layout()
        plt.savefig('Grafica_encoded.png')
        plt.close()
