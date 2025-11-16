import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { Login } from './login/login';
import { Cadastro } from './cadastro/cadastro';
import { DefinirSenha } from './definir-senha/definir-senha';
import { UploadMetadata } from './upload-metadata/upload-metadata';
import { Home } from './home/home';

export const routes: Routes = [

  { path: '', redirectTo: 'login', pathMatch: 'full' },

  { path: 'inicio', component: Home},
  { path: 'login', component: Login },
  { path: 'cadastro', component: Cadastro },
  { path: 'definir-senha', component: DefinirSenha },
  { path: 'analisar', component: UploadMetadata },

  { path: '**', redirectTo: 'login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}