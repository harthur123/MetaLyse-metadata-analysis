import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },

  { path: 'inicio', loadComponent: () => import('./home/home').then(m => m.Home) },
  { path: 'login', loadComponent: () => import('./login/login').then(m => m.Login) },
  { path: 'cadastro', loadComponent: () => import('./cadastro/cadastro').then(m => m.Cadastro) },
  { path: 'definir-senha', loadComponent: () => import('./definir-senha/definir-senha').then(m => m.DefinirSenha) },
  { path: 'analisar', loadComponent: () => import('./upload-metadata/upload-metadata').then(m => m.UploadMetadata) },

  { path: '**', redirectTo: 'login' }
];
