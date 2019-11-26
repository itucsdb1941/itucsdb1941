import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FoodListComponent } from './components/food-list/food-list.component';
import { SignComponent } from './components/sign-page/sign-page.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { NewPasswordComponent } from './components/new-password/new-password.component';
import { FoodMenuComponent } from './components/food-menu/food-menu.component';
import { DrinkMenuComponent } from './components/drink-menu/drink-menu.component';
import { DessertMenuComponent } from './components/dessert-menu/dessert-menu.component';
import { RecipeComponent } from './components/recipe/recipe.component';

const routes: Routes = [
  { path: 'sign-page', component: SignComponent },
  { path: 'foods-list', component: FoodListComponent },
  { path: 'login-page', component: LoginPageComponent },
  { path: 'new-password', component: NewPasswordComponent },
  { path: 'food-menu', component: FoodMenuComponent },
  { path: 'drink-menu', component: DrinkMenuComponent },
  { path: 'dessert-menu', component: DessertMenuComponent },
  { path: 'recipe/food/:id' , component: RecipeComponent },
  { path: 'recipe/drink/:id' , component: RecipeComponent },
  { path: 'recipe/dessert/:id' , component: RecipeComponent },
];
 
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 


}
