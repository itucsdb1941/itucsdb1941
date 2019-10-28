import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FoodListComponent } from './components/food-list/food-list.component';
import { SignComponent } from './components/sign-page/sign-page.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
//import { NewPasswordComponent } from './components/new-password/new-password.component';
const routes: Routes = [
  { path: 'sign-page', component: SignComponent },
  { path: 'foods-list', component: FoodListComponent },
  { path: 'login-page', component: LoginPageComponent },
  //{ path: 'new-password', component: NewPasswordComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 


}
