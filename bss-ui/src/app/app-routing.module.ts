import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FoodListComponent } from './components/food-list/food-list.component';
import { SignComponent } from './components/sign-page/sign-page.component';

const routes: Routes = [
  { path: 'foods-list', component: FoodListComponent },
  { path: 'sign-page', component: SignComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 


}
