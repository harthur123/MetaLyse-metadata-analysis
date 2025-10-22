import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { Cadastro } from './cadastro/cadastro';
import { HomeComponent } from './home/home';
import { Login } from './login/login';

export const routes: Routes = [
  { path: '', redirectTo: 'inicio', pathMatch: 'full' },
  { path: 'inicio', component: HomeComponent },
  { path: 'login', component: Login },
  { path: 'cadastro', component: Cadastro },
  { path: '**', redirectTo: 'inicio' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
