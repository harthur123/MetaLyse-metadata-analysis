import { ApplicationConfig, importProvidersFrom, provideZonelessChangeDetection, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations'; // ✅ Adicionado
import { HttpClientModule, provideHttpClient, withFetch } from '@angular/common/http'; // ✅ Adicionado
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    importProvidersFrom(HttpClientModule),
    provideHttpClient(withFetch()), // ✅ Necessário para o ApiService
    provideAnimations(),                   // ✅ Necessário para Angular Material
  ]
};
