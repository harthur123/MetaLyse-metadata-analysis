import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },

  { path: 'inicio', loadComponent: () => import('./home/home').then(m => m.Home) },
  { path: 'login', loadComponent: () => import('./login/login').then(m => m.Login) },
  { path: 'cadastro', loadComponent: () => import('./cadastro/cadastro').then(m => m.Cadastro) },
  { path: 'reset-password-request', loadComponent: () => import('./solicitar-redefinicao/solicitar-redefinicao').then(m => m.SolicitarRedefinicao) },
  { path: 'definir-senha', loadComponent: () => import('./definir-senha/definir-senha').then(m => m.DefinirSenha) },
  { path: 'analisar', loadComponent: () => import('./upload-metadata/upload-metadata').then(m => m.UploadMetadata) },
  { path: 'historico', loadComponent: () => import('./historico/historico').then(m => m.Historico) },

  { path: '**', redirectTo: 'login' }
];
