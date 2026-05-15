import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login').then((m) => m.LoginComponent),
  },
  {
    path: 'welcome',
    loadComponent: () =>
      import('./pages/welcome/welcome').then((m) => m.WelcomeComponent),
    canActivate: [authGuard],
  },
  {
    path: '**',
    redirectTo: 'login',
  },
];
