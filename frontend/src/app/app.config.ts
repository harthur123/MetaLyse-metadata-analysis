import { ApplicationConfig, importProvidersFrom, provideZonelessChangeDetection, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
// Remova HttpClientModule daqui, não é necessário
import { provideHttpClient, withFetch } from '@angular/common/http'; 
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    
    // REMOVA ESTA LINHA: importProvidersFrom(HttpClientModule), 
    
    provideHttpClient(withFetch()), // ✅ Este é o correto e suficiente
    provideAnimations(),            // ✅ Correto para o Material
  ]
};